# Купить может только пользователь в состоянии "shop".
# TODO: selective

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command, StateFilter
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import exceptions

from keyboards.inline.callback_datas import choose_item_callback, buy_item_callback
from keyboards.inline.outfit_shop_menus import get_choose_outfit_menu, buy_outfit_menu
from keyboards.inline.weapon_shop_menus import get_choose_weapon_menu, buy_weapon_menu
from loader import dp
from states.game_state import GameState
from states.register_state import RegisterState
from utils.db_api import weapon_commands, outfit_commands, meal_commands, inventory_weapon_commands, user_commands, \
    inventory_outfit_commands


@dp.message_handler(Command("shop"), state=GameState.registered)
async def show_items(message: types.Message, state: FSMContext):
    choose_weapon_menu = await get_choose_weapon_menu()
    await message.answer("Выберите товар из меню ниже",
                         reply_markup=choose_weapon_menu)
    await GameState.shopping.set()


@dp.callback_query_handler(text="cancel_shop", state=GameState.shopping)
async def cancel_shop(call: CallbackQuery):
    await call.message.edit_reply_markup()
    await call.answer(cache_time=15)
    await GameState.registered.set()


@dp.callback_query_handler(text="cancel_buy", state=GameState.shopping)
async def cancel_buy(call: CallbackQuery):
    await call.message.edit_text("Выберите товар из меню ниже")
    await call.message.edit_reply_markup(await get_choose_weapon_menu())
    await call.answer(cache_time=15)


@dp.callback_query_handler(choose_item_callback.filter(item_type="weapon"), state=GameState.shopping)
async def show_weapon(call: CallbackQuery, callback_data: dict):
    weapon = await weapon_commands.select_weapon(int(callback_data.get("item_id")))
    await call.message.edit_text(
        f'Название: {weapon.weapon_name}' + '\n'
        f'Цена: {weapon.weapon_price}' + '\n'
        f'Описание: {weapon.weapon_description}' + '\n'
        f'Урон: {weapon.damage}' + '\n'
        "На сколько единиц увеличивает ловкость: {}\n".format(weapon.agility_add) if weapon.agility_add != 0 else ""
        "Во сколько раз увеличивает ловкость: {}".format(weapon.agility_mpy) if weapon.agility_mpy != 1 else ""
        "На сколько единиц увеличивает здоровье: {}\n".format(weapon.health_add) if weapon.health_add != 0 else ""
        "Во сколько раз увеличивает ловкость: {}".format(weapon.health_mpy) if weapon.health_mpy != 1 else ""
    )
    buy_weapon_menu.inline_keyboard[0][0].callback_data = buy_item_callback.new(
        item_type="weapon",
        item_id=weapon.weapon_id
    )
    await call.message.edit_reply_markup(buy_weapon_menu)


@dp.callback_query_handler(buy_item_callback.filter(item_type="weapon"), state=GameState.shopping)
async def buy_weapon(call: CallbackQuery, callback_data: dict):
    weapon = await weapon_commands.select_weapon(int(callback_data.get("item_id")))
    user = await user_commands.select_user(user_id=call.from_user.id)
    if user.money < weapon.weapon_price:
        await call.answer(
            f"Вам нужно на {weapon.weapon_price - user.money} монет больше, чтобы купить этот предмет",
            cache_time=15
        )
    else:
        await inventory_weapon_commands.add_inventory_weapon(user.user_id, weapon.weapon_id)
        await user_commands.update_user_money(user.user_id, user.money - weapon.weapon_price)
    await cancel_buy(call)


@dp.callback_query_handler(text="show_items_outfit", state=GameState.shopping)
async def show_items_outfit(call: CallbackQuery):
    choose_outfit_menu = await get_choose_outfit_menu()
    await call.message.edit_reply_markup(await get_choose_outfit_menu())
    await call.answer(cache_time=15)


@dp.callback_query_handler(choose_item_callback.filter(item_type="outfit"), state=GameState.shopping)
async def show_outfit(call: CallbackQuery, callback_data: dict):
    outfit = await outfit_commands.select_outfit(int(callback_data.get("item_id")))
    await call.message.edit_text(  # TODO: собирать описание предмета для магазина в БД
        f'Название: {outfit.outfit_name}' + '\n'
        f'Цена: {outfit.outfit_price}' + '\n'
        f'Описание: {outfit.outfit_description}' + '\n'
        "На сколько единиц увеличивает ловкость: {}\n".format(outfit.agility_add) if outfit.agility_add != 0 else ""
        "Во сколько раз увеличивает ловкость: {}".format(outfit.agility_mpy) if outfit.agility_mpy != 1 else ""
        "На сколько единиц увеличивает здоровье: {}\n".format(outfit.health_add) if outfit.health_add != 0 else ""
        "Во сколько раз увеличивает ловкость: {}".format(outfit.health_mpy) if outfit.health_mpy != 1 else ""
        "На сколько единиц увеличивает здоровье: {}\n".format(outfit.strength_add) if outfit.strength_add != 0 else ""
        "Во сколько раз увеличивает ловкость: {}".format(outfit.strength_mpy) if outfit.strength_mpy != 1 else ""
    )
    buy_outfit_menu.inline_keyboard[0][0].callback_data = buy_item_callback.new(
        item_type="outfit",
        item_id=outfit.outfit_id
    )
    await call.message.edit_reply_markup(buy_outfit_menu)


@dp.callback_query_handler(buy_item_callback.filter(item_type="outfit"), state=GameState.shopping)
async def buy_outfit(call: CallbackQuery, callback_data: dict):
    outfit = await outfit_commands.select_outfit(int(callback_data.get("item_id")))
    user = await user_commands.select_user(user_id=call.from_user.id)
    if user.money < outfit.outfit_price:
        await call.answer(
            f"Вам нужно на {outfit.outfit_price - user.money} монет больше, чтобы купить этот предмет",
            cache_time=15
        )
    else:
        await inventory_outfit_commands.add_inventory_outfit(user.user_id, outfit.outfit_id)
        await user_commands.update_user_money(user.user_id, user.money - outfit.outfit_price)
    await cancel_buy(call)
