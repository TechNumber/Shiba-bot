import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import CallbackQuery

from filters import IsCalledByOwner
from keyboards.inline.callback_datas import discard_item_callback, \
    cancel_callback, show_inventory_items_callback, show_item_callback, equip_item_callback
from keyboards.inline.inventory.home_inventory_menus import get_home_inventory_menu
from keyboards.inline.inventory.meal_inventory_menus import get_inventory_all_meals_menu, get_inventory_meal_menu
from keyboards.inline.inventory.outfit_inventory_menus import get_inventory_all_outfits_menu, get_inventory_outfit_menu
from keyboards.inline.inventory.weapon_inventory_menus import get_inventory_all_weapons_menu, get_inventory_weapon_menu
from loader import dp
from states.game_state import GameState
from utils.db_api import weapon_commands, outfit_commands, inventory_weapon_commands, user_commands, \
    inventory_outfit_commands, meal_commands, inventory_meal_commands


# TODO: только пользователь, вызвавший инвентарь, может выполнять в нём действия


@dp.message_handler(Command("inventory"), state=GameState.registered)
async def show_inventory_categories(message: types.Message, state: FSMContext):
    await message.answer("Выберите категорию предметов",
                         reply_markup=await get_home_inventory_menu(user_id=message.from_user.id))
    await GameState.inventory.set()


@dp.callback_query_handler(IsCalledByOwner(), cancel_callback.filter(cancel_type="inventory"),
                           state=GameState.inventory)
async def cancel_inventory(call: CallbackQuery):
    await call.message.edit_reply_markup()
    await GameState.registered.set()
    await call.answer(cache_time=15)


@dp.callback_query_handler(IsCalledByOwner(), cancel_callback.filter(cancel_type="show"),
                           state=GameState.inventory)
async def cancel_show_items(call: CallbackQuery):
    await call.message.edit_text("Выберите категорию предметов")
    await call.message.edit_reply_markup(await get_home_inventory_menu(user_id=call.from_user.id))


@dp.callback_query_handler(IsCalledByOwner(), cancel_callback.filter(cancel_type="equip_weapon"),
                           state=GameState.inventory)
async def cancel_equip_weapon(call: CallbackQuery):
    await show_inventory_weapons(call)


@dp.callback_query_handler(IsCalledByOwner(), show_inventory_items_callback.filter(item_type="weapon"),
                           state=GameState.inventory)
async def show_inventory_weapons(call: CallbackQuery):
    await call.message.edit_text("Выберите оружие, которое хотите экипировать")
    await call.message.edit_reply_markup(await get_inventory_all_weapons_menu(user_id=call.from_user.id))
    await call.answer(cache_time=15)


@dp.callback_query_handler(IsCalledByOwner(), show_item_callback.filter(item_type="weapon"),
                           state=GameState.inventory)
async def show_weapon(call: CallbackQuery, callback_data: dict):
    weapon = await weapon_commands.select_weapon(int(callback_data.get("item_id")))
    await call.message.edit_text(weapon.weapon_chars)
    await call.message.edit_reply_markup(
        await get_inventory_weapon_menu(user_id=call.from_user.id, weapon_id=weapon.weapon_id))


@dp.callback_query_handler(IsCalledByOwner(), equip_item_callback.filter(item_type="weapon"), state=GameState.inventory)
async def equip_weapon(call: CallbackQuery, callback_data: dict):
    weapon = await weapon_commands.select_weapon(int(callback_data.get("item_id")))
    user = await user_commands.select_user(user_id=call.from_user.id)
    await user_commands.update_user_weapon(user_id=user.user_id, weapon_id=weapon.weapon_id)
    await show_inventory_weapons(call)


@dp.callback_query_handler(IsCalledByOwner(), discard_item_callback.filter(item_type="weapon"),
                           state=GameState.inventory)
async def discard_weapon(call: CallbackQuery, callback_data: dict):
    weapon = await weapon_commands.select_weapon(int(callback_data.get("item_id")))
    user = await user_commands.select_user(user_id=call.from_user.id)
    await inventory_weapon_commands.discard_inventory_weapon(user_id=user.user_id, weapon_id=weapon.weapon_id)
    await show_inventory_weapons(call)


@dp.callback_query_handler(IsCalledByOwner(), cancel_callback.filter(cancel_type="equip_outfit"),
                           state=GameState.inventory)
async def cancel_equip_outfit(call: CallbackQuery):
    await show_inventory_outfits(call)


@dp.callback_query_handler(IsCalledByOwner(), show_inventory_items_callback.filter(item_type="outfit"),
                           state=GameState.inventory)
async def show_inventory_outfits(call: CallbackQuery):
    await call.message.edit_text("Выберите одежду, которое хотите надеть")
    await call.message.edit_reply_markup(await get_inventory_all_outfits_menu(user_id=call.from_user.id))
    await call.answer(cache_time=15)


@dp.callback_query_handler(IsCalledByOwner(), show_item_callback.filter(item_type="outfit"),
                           state=GameState.inventory)
async def show_outfit(call: CallbackQuery, callback_data: dict):
    outfit = await outfit_commands.select_outfit(int(callback_data.get("item_id")))
    await call.message.edit_text(outfit.outfit_chars)
    await call.message.edit_reply_markup(
        await get_inventory_outfit_menu(user_id=call.from_user.id, outfit_id=outfit.outfit_id))


@dp.callback_query_handler(IsCalledByOwner(), equip_item_callback.filter(item_type="outfit"), state=GameState.inventory)
async def equip_outfit(call: CallbackQuery, callback_data: dict):
    outfit = await outfit_commands.select_outfit(int(callback_data.get("item_id")))
    user = await user_commands.select_user(user_id=call.from_user.id)
    await user_commands.update_user_outfit(user_id=user.user_id, outfit_id=outfit.outfit_id)
    await show_inventory_outfits(call)


@dp.callback_query_handler(IsCalledByOwner(), discard_item_callback.filter(item_type="outfit"),
                           state=GameState.inventory)
async def discard_outfit(call: CallbackQuery, callback_data: dict):
    outfit = await outfit_commands.select_outfit(int(callback_data.get("item_id")))
    user = await user_commands.select_user(user_id=call.from_user.id)
    await inventory_outfit_commands.discard_inventory_outfit(user_id=user.user_id, outfit_id=outfit.outfit_id)
    await show_inventory_outfits(call)


@dp.callback_query_handler(IsCalledByOwner(), cancel_callback.filter(cancel_type="eat_meal"),
                           state=GameState.inventory)
async def cancel_eat_meal(call: CallbackQuery):
    await show_inventory_meals(call)


@dp.callback_query_handler(IsCalledByOwner(), show_inventory_items_callback.filter(item_type="meal"),
                           state=GameState.inventory)
async def show_inventory_meals(call: CallbackQuery):
    """
    Выводит меню из кнопок, позволяющих выбрать блюдо из тех, что находятся в данный
    момент в инвентаре у пользователя.

    Filters:
        IsCalledByOwner(): Кнопка, вызвавшая CallbackQuery, была нажата тем же
        пользователем, который изначально вызвал меню инвентаря.
        show_inventory_items_callback.filter(item_type="meal"): CallbackData вызванного
        Callback относится к типу show_inventory_items_callback, т.е. отвечает за вывод
        предметов инвентаря. Тип предметов — еда.

    Args:
        call (CallbackQuery): Callback кнопки "еда", содержащий CallbackData
        для кнопок отображения содержимого инвентаря определённого типа.

    Returns:
        None

    """
    """
    Generators have a ``Yields`` section instead of a ``Returns`` section.

    Args:
        n (int): The upper limit of the range to generate, from 0 to `n` - 1.

    Yields:
        int: The next number in the range of 0 to `n` - 1.

    Examples:
        Examples should be written in doctest format, and should illustrate how
        to use the function.
    """

    '''
        Returns the reversed String.

        Parameters:
            str1 (str):The string which is to be reversed.

        Returns:
            reverse(str1):The string which gets reversed.   
        '''
    await call.message.edit_text("Выберите, чем хотите подкрепиться")
    await call.message.edit_reply_markup(await get_inventory_all_meals_menu(user_id=call.from_user.id))
    await call.answer(cache_time=15)


@dp.callback_query_handler(IsCalledByOwner(), show_item_callback.filter(item_type="meal"),
                           state=GameState.inventory)
async def show_meal(call: CallbackQuery, callback_data: dict):
    meal = await meal_commands.select_meal(int(callback_data.get("item_id")))
    await call.message.edit_text(meal.meal_chars)
    await call.message.edit_reply_markup(
        await get_inventory_meal_menu(user_id=call.from_user.id, meal_id=meal.meal_id))


@dp.callback_query_handler(IsCalledByOwner(), equip_item_callback.filter(item_type="meal"), state=GameState.inventory)
async def eat_meal(call: CallbackQuery, callback_data: dict):
    meal = await meal_commands.select_meal(int(callback_data.get("item_id")))
    user = await user_commands.select_user(user_id=call.from_user.id)
    tasks = [
        meal_commands.apply_meal_effects(user_id=user.user_id, meal_id=meal.meal_id),
        inventory_meal_commands.discard_inventory_meal(user_id=user.user_id, meal_id=meal.meal_id),
        show_inventory_meals(call)
    ]
    await asyncio.gather(*tasks)


@dp.callback_query_handler(IsCalledByOwner(), discard_item_callback.filter(item_type="meal"),
                           state=GameState.inventory)
async def discard_meal(call: CallbackQuery, callback_data: dict):
    meal = await meal_commands.select_meal(int(callback_data.get("item_id")))
    user = await user_commands.select_user(user_id=call.from_user.id)
    await inventory_meal_commands.discard_inventory_meal(user_id=user.user_id, meal_id=meal.meal_id)
    await show_inventory_meals(call)
