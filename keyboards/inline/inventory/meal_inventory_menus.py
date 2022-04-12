import math

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import discard_item_callback, cancel_callback, \
    equip_item_callback, show_item_callback
from utils.db_api import inventory_meal_commands


async def get_inventory_all_meals_menu(user_id: int):
    inventory_meals_menu = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Отмена",
                    callback_data=cancel_callback.new(
                        user_id=user_id,
                        cancel_type="show"
                    )
                )
            ]
        ],
        resize_keyboard=True
    )
    meals = await inventory_meal_commands.select_all_meals_by_user_id(user_id=user_id)
    meal_buttons = [InlineKeyboardButton(
        text="{}, {} шт.".format(
            meal.meal_name,
            await inventory_meal_commands.get_meal_amount(user_id=user_id, meal_id=meal.meal_id)
        ),
        callback_data=show_item_callback.new(
            user_id=user_id,
            item_type="meal",
            item_id=meal.meal_id
        )
    ) for meal in meals]
    meal_rows = [meal_buttons[i * 2:i * 2 + 2] for i in range(math.ceil(len(meal_buttons) / 2))]
    for row in meal_rows:
        inventory_meals_menu.inline_keyboard.insert(-1, row)
    return inventory_meals_menu


async def get_inventory_meal_menu(user_id: int, meal_id: int):
    eat_meal_menu = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Съесть",
                    callback_data=equip_item_callback.new(
                        user_id=user_id,
                        item_type="meal",
                        item_id=meal_id
                    )
                ),
                InlineKeyboardButton(
                    text="Выбросить",
                    callback_data=discard_item_callback.new(
                        user_id=user_id,
                        item_type="meal",
                        item_id=meal_id
                    )
                ),
                InlineKeyboardButton(
                    text="Отмена",
                    callback_data=cancel_callback.new(
                        user_id=user_id,
                        cancel_type="eat_meal"
                    )
                )
            ],
        ],
        resize_keyboard=True
    )
    return eat_meal_menu

# TODO: пометка "(Выбрано)", если предмет уже выбран
