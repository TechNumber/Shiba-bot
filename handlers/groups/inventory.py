import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import CallbackQuery

from filters import IsCalledByOwner
from keyboards.inline.callback_datas import discard_item_callback, \
    cancel_callback, show_inventory_items_callback, show_item_callback, equip_item_callback, call_service_callback
from keyboards.inline.inventory.home_inventory_menus import get_home_inventory_menu
from keyboards.inline.inventory.meal_inventory_menus import get_inventory_all_meals_menu, get_inventory_meal_menu
from keyboards.inline.inventory.outfit_inventory_menus import get_inventory_all_outfits_menu, get_inventory_outfit_menu
from keyboards.inline.inventory.weapon_inventory_menus import get_inventory_all_weapons_menu, get_inventory_weapon_menu
from loader import dp
from states.game_state import GameState
from utils.db_api import weapon_commands, outfit_commands, inventory_weapon_commands, user_commands, \
    inventory_outfit_commands, meal_commands, inventory_meal_commands, effect_commands

# TODO: только пользователь, вызвавший инвентарь, может выполнять в нём действия
from utils.db_api.db_gino import db


@dp.message_handler(Command("inventory"), state=GameState.registered)
async def show_inventory_categories(message: types.Message):
    """
    Выводит сообщение с тремя кнопками: "Оружие", "Одежда", "Еда", позволяющими
    выбрать категорию предметов инвентаря, в которую хочет перейти пользователь,
    а также с кнопкой "Отмена".

    Filters:
        Command("inventory"): сообщение содержит команду /inventory.
        state=GameState.registered: пользователь, вызвавший команду, участвует в игре

    Args:
        message (types.Message): Сообщение с командой /inventory

    Returns:
        None
    """
    await message.answer("Выберите категорию предметов",
                         reply_markup=await get_home_inventory_menu(user_id=message.from_user.id))
    await GameState.inventory.set()


@dp.callback_query_handler(IsCalledByOwner(), call_service_callback.filter(service_type="inventory"),
                           state=GameState.registered)
async def show_inventory_categories_from_callback(call: types.CallbackQuery):
    await call.message.answer("Выберите категорию предметов",
                              reply_markup=await get_home_inventory_menu(user_id=call.from_user.id))
    await GameState.inventory.set()


@dp.callback_query_handler(IsCalledByOwner(), cancel_callback.filter(cancel_type="inventory"),
                           state=GameState.inventory)
async def cancel_inventory(call: CallbackQuery):
    """
    Закрывает меню инвентаря по нажатии кнопки "Отмена".

    Filters:
        IsCalledByOwner(): Кнопка, вызвавшая CallbackQuery, была нажата тем же
        пользователем, который изначально вызвал меню инвентаря.
        cancel_callback.filter(cancel_type="inventory"): CallbackData вызванного
        CallbackQuery относится к типу cancel_callback, т.е. отвечает за закрытие меню.
        Тип закрываемого меню — меню выбора категории предметов инвентаря.
        state=GameState.inventory: пользователь, нажавший на кнопку, находится в
        инвентаре.

    Args:
        call (CallbackQuery): CallbackQuery кнопки "Отмена", содержащий CallbackData
        для кнопок закрытия меню.

    Returns:
        None
    """
    await call.message.edit_reply_markup()
    await GameState.registered.set()
    await call.answer(cache_time=15)


@dp.callback_query_handler(IsCalledByOwner(), cancel_callback.filter(cancel_type="show"),
                           state=GameState.inventory)
async def cancel_show_items(call: CallbackQuery):
    """
    Закрывает меню с кнопками предметов в инвентаре по нажатии кнопки "Отмена".

    Filters:
        IsCalledByOwner(): Кнопка, вызвавшая CallbackQuery, была нажата тем же
        пользователем, который изначально вызвал меню инвентаря.
        cancel_callback.filter(cancel_type="show"): CallbackData вызванного
        CallbackQuery относится к типу cancel_callback, т.е. отвечает за закрытие меню.
        Тип закрываемого меню — меню с кнопками предметов в инвентаре.
        state=GameState.inventory: пользователь, нажавший на кнопку, находится в
        инвентаре.

    Args:
        call (CallbackQuery): CallbackQuery кнопки "Отмена", содержащий CallbackData
        для кнопок закрытия меню.

    Returns:
        None
    """
    await call.message.edit_text("Выберите категорию предметов")
    await call.message.edit_reply_markup(await get_home_inventory_menu(user_id=call.from_user.id))


@dp.callback_query_handler(IsCalledByOwner(), cancel_callback.filter(cancel_type="equip_weapon"),
                           state=GameState.inventory)
async def cancel_equip_weapon(call: CallbackQuery):
    """
    Закрывает меню экипировки оружия по нажатии кнопки "Отмена".

    Filters:
        IsCalledByOwner(): Кнопка, вызвавшая CallbackQuery, была нажата тем же
        пользователем, который изначально вызвал меню инвентаря.
        cancel_callback.filter(cancel_type="equip_weapon"): CallbackData вызванного
        CallbackQuery относится к типу cancel_callback, т.е. отвечает за закрытие меню.
        Тип закрываемого меню — меню экипировки оружия.
        state=GameState.inventory: пользователь, нажавший на кнопку, находится в
        инвентаре.

    Args:
        call (CallbackQuery): CallbackQuery кнопки "Отмена", содержащий CallbackData
        для кнопок закрытия меню.

    Returns:
        None
    """
    await show_inventory_weapons(call)


@dp.callback_query_handler(IsCalledByOwner(), show_inventory_items_callback.filter(item_type="weapon"),
                           state=GameState.inventory)
async def show_inventory_weapons(call: CallbackQuery):
    """
    Показывает меню выбора с кнопками оружия, содержащегося в инвентаре, и кнопкой "Отмена".

    Filters:
        IsCalledByOwner(): Кнопка, вызвавшая CallbackQuery, была нажата тем же
        пользователем, который изначально вызвал меню инвентаря.
        show_inventory_items_callback.filter(item_type="weapon"): CallbackData вызванного
        CallbackQuery относится к типу show_inventory_items_callback, т.е. отвечает за
        показ меню с кнопками предметов в инвентаре. Тип меню — меню выбора с кнопками оружия.
        state=GameState.inventory: пользователь, нажавший на кнопку, находится в
        инвентаре.

    Args:
        call (CallbackQuery): CallbackQuery кнопки "Оружие", содержащий CallbackData
        для кнопок, открывающих меню выбора с кнопками оружия.

    Returns:
        None
    """
    await call.message.edit_text("Выберите оружие, которое хотите экипировать")
    await call.message.edit_reply_markup(await get_inventory_all_weapons_menu(user_id=call.from_user.id))
    await call.answer(cache_time=15)


@dp.callback_query_handler(IsCalledByOwner(), show_item_callback.filter(item_type="weapon"),
                           state=GameState.inventory)
async def show_weapon(call: CallbackQuery, callback_data: dict):
    """
    Показывает меню экипировки выбранного оружия с его описанием и кнопками "Экипировать"
    и "Отмена"

    Filters:
        IsCalledByOwner(): Кнопка, вызвавшая CallbackQuery, была нажата тем же
        пользователем, который изначально вызвал меню инвентаря.
        show_item_callback.filter(item_type="weapon"): CallbackData вызванного
        CallbackQuery относится к типу show_item_callback, т.е. отвечает за
        показ меню выбранного предмета. Тип меню — меню выбранного оружия.
        state=GameState.inventory: пользователь, нажавший на кнопку, находится в
        инвентаре.

    Args:
        call (CallbackQuery): CallbackQuery кнопки выбранного оружия, содержащий CallbackData
        для кнопок, открывающих меню выбранного оружия.
        callback_data (dict): CallbackData пришедшего call

    Returns:
        None
    """
    weapon = await weapon_commands.select_weapon(int(callback_data.get("item_id")))
    await call.message.edit_text(weapon.weapon_chars)
    await call.message.edit_reply_markup(
        await get_inventory_weapon_menu(user_id=call.from_user.id, weapon_id=weapon.weapon_id))


@dp.callback_query_handler(IsCalledByOwner(), equip_item_callback.filter(item_type="weapon"), state=GameState.inventory)
async def equip_weapon(call: CallbackQuery, callback_data: dict):
    """
    Данный обработчик отвечает за экипировку выбранного оружия по нажатии кнопки "Экипировать".
    Т.е. данное оружие вносится в поле weapon_id записи о пользователе, отображающее, какое
    оружие сейчас у него в руках.

    Filters:
        IsCalledByOwner(): Кнопка, вызвавшая CallbackQuery, была нажата тем же
        пользователем, который изначально вызвал меню инвентаря.
        equip_item_callback.filter(item_type="weapon"): CallbackData вызванного
        CallbackQuery относится к типу equip_item_callback, т.е. отвечает за
        экипировку выбранного предмета. Тип экипируемого предмета — оружие.
        state=GameState.inventory: пользователь, нажавший на кнопку, находится в
        инвентаре.

    Args:
        call (CallbackQuery): CallbackQuery кнопки "Экипировать" выбранного оружия, содержащий
        CallbackData для кнопок, обрабатывающих экипировку предметов.
        callback_data (dict): CallbackData пришедшего call

    Returns:
        None
    """
    weapon = await weapon_commands.select_weapon(int(callback_data.get("item_id")))
    user = await user_commands.select_user(user_id=call.from_user.id)
    await user_commands.update_user_weapon(user_id=user.user_id, weapon_id=weapon.weapon_id)
    await show_inventory_weapons(call)


@dp.callback_query_handler(IsCalledByOwner(), discard_item_callback.filter(item_type="weapon"),
                           state=GameState.inventory)
async def discard_weapon(call: CallbackQuery, callback_data: dict):
    """
    Данный обработчик отвечает за удаление предмета из инвентаря по нажатии кнопки
    "Выбросить".

    Filters:
        IsCalledByOwner(): Кнопка, вызвавшая CallbackQuery, была нажата тем же
        пользователем, который изначально вызвал меню инвентаря.
        discard_item_callback.filter(item_type="weapon"): CallbackData вызванного
        CallbackQuery относится к типу discard_item_callback, т.е. отвечает за
        удаление выбранного предмета из инвентаря. Тип удаляемого предмета — оружие.
        state=GameState.inventory: пользователь, нажавший на кнопку, находится в
        инвентаре.

    Args:
        call (CallbackQuery): CallbackQuery кнопки "Выбросить" выбранного оружия,
        содержащий CallbackData для кнопок, обрабатывающих удаление предметов.
        callback_data (dict): CallbackData пришедшего call

    Returns:
        None
    """
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
        CallbackQuery относится к типу show_inventory_items_callback, т.е. отвечает
        за вывод предметов инвентаря. Тип предметов — еда.

    Args:
        call (CallbackQuery): CallbackQuery кнопки "еда", содержащий CallbackData
        для кнопок отображения содержимого инвентаря определённого типа.

    Returns:
        None
    """
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
    await effect_commands.add_effect(user=user, meal=meal),
    await inventory_meal_commands.discard_inventory_meal(user_id=user.user_id, meal_id=meal.meal_id),
    await show_inventory_meals(call)


@dp.callback_query_handler(IsCalledByOwner(), discard_item_callback.filter(item_type="meal"),
                           state=GameState.inventory)
async def discard_meal(call: CallbackQuery, callback_data: dict):
    meal = await meal_commands.select_meal(int(callback_data.get("item_id")))
    user = await user_commands.select_user(user_id=call.from_user.id)
    await inventory_meal_commands.discard_inventory_meal(user_id=user.user_id, meal_id=meal.meal_id)
    await show_inventory_meals(call)
