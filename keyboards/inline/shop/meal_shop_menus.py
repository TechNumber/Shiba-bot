import math

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import show_shop_items_callback, cancel_callback, show_item_callback, \
    buy_item_callback
from utils.db_api import meal_commands


async def get_shop_all_meals_menu(user_id: int):
    """
    Данная функция формирует и возвращает меню из кнопок, позволяющее выбрать
    одно из блюд, продающихся в магазине.

    Args:
        user_id (int): id пользователя; оно помещается в CallbackData каждой кнопки
        для последующей проверки фильтром IsCalledByOwner(). Благодаря этому
        нажатие других пользователей на кнопки, предназначенные для данного пользователя,
        не будут обрабатываться.

    Returns:
        (InlineKeyboardMarkup): Меню выбора блюда в магазине.
    """
    show_meals_menu = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Одежда",
                    callback_data=show_shop_items_callback.new(
                        user_id=user_id,
                        item_type="outfit"
                    )
                ),
                InlineKeyboardButton(
                    text="Отмена",
                    callback_data=cancel_callback.new(
                        user_id=user_id,
                        cancel_type="shop"
                    )
                )
            ]
        ],
        resize_keyboard=True
    )
    meals = await meal_commands.select_all_meals()
    meal_buttons = [InlineKeyboardButton(
        text=meal.meal_name,
        callback_data=show_item_callback.new(
            user_id=user_id,
            item_type="meal",
            item_id=meal.meal_id
        )
    ) for meal in meals]
    meal_rows = [meal_buttons[i * 2:i * 2 + 2] for i in range(math.ceil(len(meal_buttons) / 2))]
    for row in meal_rows:
        show_meals_menu.inline_keyboard.insert(-1, row)
    return show_meals_menu


async def get_shop_meal_menu(user_id: int, meal_id: int):
    """
    Данная функция формирует и возвращает меню выбранного блюда с кнопками
    "Купить", "Выбросить", "Отмена".

    Args:
        user_id (int): id пользователя; оно помещается в CallbackData каждой кнопки
        для последующей проверки фильтром IsCalledByOwner(). Благодаря этому
        нажатие других пользователей на кнопки, предназначенные для данного пользователя,
        не будут обрабатываться.
        meal_id (int): id выбранного блюда; по нему будет осуществляться извлечение
        блюда и его характеристик из БД.

    Returns:
        (InlineKeyboardMarkup): Меню выбранного блюда.
    """
    meal_menu = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Купить",
                    callback_data=buy_item_callback.new(
                        user_id=user_id,
                        item_type="meal",
                        item_id=meal_id
                    )
                ),
                InlineKeyboardButton(
                    text="Отмена",
                    callback_data=cancel_callback.new(
                        user_id=user_id,
                        cancel_type="buy"
                    )
                )
            ],
        ],
        resize_keyboard=True
    )
    return meal_menu
