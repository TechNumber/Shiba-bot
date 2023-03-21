from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import CallbackQuery

from filters import IsCalledByOwner
from keyboards.inline.callback_datas import buy_item_callback, cancel_callback, show_item_callback, \
    show_shop_items_callback, call_service_callback
from keyboards.inline.shop.meal_shop_menus import get_shop_all_meals_menu, get_shop_meal_menu
from keyboards.inline.shop.outfit_shop_menus import get_shop_all_outfits_menu, get_shop_outfit_menu
from keyboards.inline.shop.weapon_shop_menus import get_shop_all_weapons_menu, get_shop_weapon_menu
from loader import dp
from states.game_state import GameState
from utils.db_api import weapon_commands, outfit_commands, meal_commands, inventory_weapon_commands, user_commands, \
    inventory_outfit_commands, inventory_meal_commands
from utils.db_api.db_gino import db


@dp.message_handler(Command("shop"), state=GameState.registered)
async def show_shop_weapons(message: types.Message):
    shop_weapons_menu = await get_shop_all_weapons_menu(user_id=message.from_user.id)
    await message.answer("Выберите товар из меню ниже",
                         reply_markup=shop_weapons_menu)
    await GameState.shopping.set()


@dp.callback_query_handler(IsCalledByOwner(), call_service_callback.filter(service_type="shop"),
                           state=GameState.registered)
async def show_shop_weapons_from_callback(call: CallbackQuery):
    shop_weapons_menu = await get_shop_all_weapons_menu(user_id=call.from_user.id)
    await call.message.answer("Выберите товар из меню ниже",
                              reply_markup=shop_weapons_menu)
    await GameState.shopping.set()
    await call.answer(cache_time=15)


@dp.callback_query_handler(IsCalledByOwner(), cancel_callback.filter(cancel_type="shop"), state=GameState.shopping)
async def cancel_shop(call: CallbackQuery):
    await call.message.edit_reply_markup()
    await call.answer(cache_time=15)
    await GameState.registered.set()


@dp.callback_query_handler(IsCalledByOwner(), cancel_callback.filter(cancel_type="buy"), state=GameState.shopping)
async def cancel_buy(call: CallbackQuery):
    await call.message.edit_text("Выберите товар из меню ниже")
    await call.message.edit_reply_markup(await get_shop_all_weapons_menu(user_id=call.from_user.id))
    await call.answer(cache_time=15)


@dp.callback_query_handler(IsCalledByOwner(), show_item_callback.filter(item_type="weapon"), state=GameState.shopping)
async def show_weapon(call: CallbackQuery, callback_data: dict):
    weapon = await weapon_commands.select_weapon(int(callback_data.get("item_id")))
    await call.message.edit_text(weapon.weapon_chars)
    await call.message.edit_reply_markup(
        await get_shop_weapon_menu(user_id=call.from_user.id, weapon_id=weapon.weapon_id))


@dp.callback_query_handler(IsCalledByOwner(), buy_item_callback.filter(item_type="weapon"), state=GameState.shopping)
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


@dp.callback_query_handler(IsCalledByOwner(), show_shop_items_callback.filter(item_type="outfit"),
                           state=GameState.shopping)
async def show_shop_outfits(call: CallbackQuery):
    await call.message.edit_reply_markup(await get_shop_all_outfits_menu(user_id=call.from_user.id))
    await call.answer(cache_time=15)


@dp.callback_query_handler(IsCalledByOwner(), show_item_callback.filter(item_type="outfit"), state=GameState.shopping)
async def show_outfit(call: CallbackQuery, callback_data: dict):
    outfit = await outfit_commands.select_outfit(int(callback_data.get("item_id")))
    await call.message.edit_text(outfit.outfit_chars)
    await call.message.edit_reply_markup(
        await get_shop_outfit_menu(user_id=call.from_user.id, outfit_id=outfit.outfit_id))


@dp.callback_query_handler(IsCalledByOwner(), buy_item_callback.filter(item_type="outfit"), state=GameState.shopping)
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


@dp.callback_query_handler(IsCalledByOwner(), show_shop_items_callback.filter(item_type="meal"),
                           state=GameState.shopping)
async def show_shop_meals(call: CallbackQuery):
    await call.message.edit_reply_markup(await get_shop_all_meals_menu(user_id=call.from_user.id))
    await call.answer(cache_time=15)


@dp.callback_query_handler(IsCalledByOwner(), show_item_callback.filter(item_type="meal"), state=GameState.shopping)
async def show_meal(call: CallbackQuery, callback_data: dict):
    meal = await meal_commands.select_meal(int(callback_data.get("item_id")))
    await call.message.edit_text(meal.meal_chars)
    await call.message.edit_reply_markup(await get_shop_meal_menu(user_id=call.from_user.id, meal_id=meal.meal_id))


@dp.callback_query_handler(IsCalledByOwner(), buy_item_callback.filter(item_type="meal"), state=GameState.shopping)
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
