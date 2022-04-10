import math

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import buy_item_callback, cancel_callback, \
    show_shop_items_callback, show_item_callback
from utils.db_api import weapon_commands


async def get_shop_all_weapons_menu(user_id: int):
    shop_all_weapons_menu = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Отмена",
                    callback_data=cancel_callback.new(
                        user_id=user_id,
                        cancel_type="shop"
                    )
                ),
                InlineKeyboardButton(
                    text="Одежда",
                    callback_data=show_shop_items_callback.new(
                        user_id=user_id,
                        item_type="outfit"
                    )
                )
            ]
        ],
        resize_keyboard=True
    )
    weapons = await weapon_commands.select_all_weapons()
    weapon_buttons = [InlineKeyboardButton(
        text=weapon.weapon_name,
        callback_data=show_item_callback.new(
            user_id=user_id,
            item_type="weapon",
            item_id=weapon.weapon_id
        )
    ) for weapon in weapons]
    weapon_rows = [weapon_buttons[i * 2:i * 2 + 2] for i in range(math.ceil(len(weapon_buttons) / 2))]
    for row in weapon_rows:
        shop_all_weapons_menu.inline_keyboard.insert(-1, row)
    return shop_all_weapons_menu


async def get_shop_weapon_menu(user_id: int, weapon_id: int):
    shop_weapon_menu = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Купить",
                    callback_data=buy_item_callback.new(
                        user_id=user_id,
                        item_type="weapon",
                        item_id=weapon_id
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
    return shop_weapon_menu
