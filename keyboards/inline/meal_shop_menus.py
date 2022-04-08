import math

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import choose_item_callback
from utils.db_api import meal_commands


async def get_choose_meal_menu():
    choose_meal_menu = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Одежда",
                    callback_data="show_items_outfit"
                ),
                InlineKeyboardButton(
                    text="Отмена",
                    callback_data="cancel_shop"
                )
            ]
        ],
        resize_keyboard=True
    )
    meals = await meal_commands.select_all_meals()
    meal_buttons = [InlineKeyboardButton(
        text=meal.meal_name,
        callback_data=choose_item_callback.new(
            item_type="meal",
            item_id=meal.meal_id
        )
    ) for meal in meals]
    meal_rows = [meal_buttons[i * 2:i * 2 + 2] for i in range(math.ceil(len(meal_buttons) / 2))]
    for row in meal_rows:
        choose_meal_menu.inline_keyboard.insert(-1, row)
    return choose_meal_menu


buy_meal_menu = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Купить",
                callback_data=choose_item_callback.new(
                    item_type="meal",
                    item_id=-1
                )
            ),
            InlineKeyboardButton(
                text="Отмена",
                callback_data="cancel_buy"
            )
        ],
    ],
    resize_keyboard=True
)
