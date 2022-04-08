import math

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import choose_item_callback
from utils.db_api import weapon_commands


async def get_choose_weapon_menu():
    choose_weapon_menu = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Отмена",
                    callback_data="cancel_shop"
                ),
                InlineKeyboardButton(
                    text="Одежда",
                    callback_data="show_items_outfit"
                )
            ]
        ],
        resize_keyboard=True#,
        #selective=True
    )
    weapons = await weapon_commands.select_all_weapons()
    weapon_buttons = [InlineKeyboardButton(
        text=weapon.weapon_name,
        callback_data=choose_item_callback.new(
            item_type="weapon",
            item_id=weapon.weapon_id
        )
    ) for weapon in weapons]
    weapon_rows = [weapon_buttons[i * 2:i * 2 + 2] for i in range(math.ceil(len(weapon_buttons) / 2))]
    for row in weapon_rows:
        choose_weapon_menu.inline_keyboard.insert(-1, row)
    return choose_weapon_menu


buy_weapon_menu = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Купить",
                callback_data=choose_item_callback.new(
                    item_type="weapon",
                    item_id=-1
                )
            ),
            InlineKeyboardButton(
                text="Отмена",
                callback_data="cancel_buy"
            )
        ],
    ],
    resize_keyboard=True#,
    #selective=True
)
