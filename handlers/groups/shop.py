from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command, StateFilter
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import exceptions

from keyboards.inline.callback_datas import choose_item_callback, buy_item_callback
from keyboards.inline.meal_shop_menus import get_choose_meal_menu, buy_meal_menu
from keyboards.inline.outfit_shop_menus import get_choose_outfit_menu, buy_outfit_menu
from keyboards.inline.weapon_shop_menus import get_choose_weapon_menu, buy_weapon_menu
from loader import dp
from states.game_state import GameState
from states.register_state import RegisterState
from utils.db_api import weapon_commands, outfit_commands, meal_commands, inventory_weapon_commands, user_commands, \
    inventory_outfit_commands, inventory_meal_commands


# TODO: только пользователь, вызвавший магазин, может покупать в нём что-то. Реализация:
# проверять, совпадают ли id пользователя, вызвавшего магазин, и пользователя,
# нажавшего кнопку магазина. Либо записывать в информацию состояния id пользователя и
# фильтровать по нему в фильтре состояния


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
    await call.message.edit_text(weapon.weapon_chars)
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
    await call.message.edit_reply_markup(await get_choose_outfit_menu())
    await call.answer(cache_time=15)


@dp.callback_query_handler(choose_item_callback.filter(item_type="outfit"), state=GameState.shopping)
async def show_outfit(call: CallbackQuery, callback_data: dict):
    outfit = await outfit_commands.select_outfit(int(callback_data.get("item_id")))
    await call.message.edit_text(outfit.outfit_chars)
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


@dp.callback_query_handler(text="show_items_meal", state=GameState.shopping)
async def show_items_meal(call: CallbackQuery):
    await call.message.edit_reply_markup(await get_choose_meal_menu())
    await call.answer(cache_time=15)


@dp.callback_query_handler(choose_item_callback.filter(item_type="meal"), state=GameState.shopping)
async def show_meal(call: CallbackQuery, callback_data: dict):
    meal = await meal_commands.select_meal(int(callback_data.get("item_id")))
    await call.message.edit_text(meal.meal_chars)
    buy_meal_menu.inline_keyboard[0][0].callback_data = buy_item_callback.new(
        item_type="meal",
        item_id=meal.meal_id
    )
    await call.message.edit_reply_markup(buy_meal_menu)


@dp.callback_query_handler(buy_item_callback.filter(item_type="meal"), state=GameState.shopping)
async def buy_meal(call: CallbackQuery, callback_data: dict):
    meal = await meal_commands.select_meal(int(callback_data.get("item_id")))
    user = await user_commands.select_user(user_id=call.from_user.id)
    if user.money < meal.meal_price:
        await call.answer(
            f"Вам нужно на {meal.meal_price - user.money} монет больше, чтобы купить этот предмет",
            cache_time=15
        )
    else:
        await inventory_meal_commands.add_inventory_meal(user.user_id, meal.meal_id)
        await user_commands.update_user_money(user.user_id, user.money - meal.meal_price)
    await cancel_buy(call)
