import math

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import choose_item_callback
from utils.db_api import outfit_commands


async def get_choose_outfit_menu():
    choose_outfit_menu = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Оружие",
                    callback_data="cancel_buy"
                ),
                InlineKeyboardButton(
                    text="Отмена",
                    callback_data="cancel_shop"
                ),
                InlineKeyboardButton(
                    text="Еда",
                    callback_data="show_items_meal"
                )
            ]
        ],
        resize_keyboard=True
    )
    outfits = await outfit_commands.select_all_outfits()
    outfit_buttons = [InlineKeyboardButton(
        text=outfit.outfit_name,
        callback_data=choose_item_callback.new(
            item_type="outfit",
            item_id=outfit.outfit_id
        )
    ) for outfit in outfits]
    outfit_rows = [outfit_buttons[i * 2:i * 2 + 2] for i in range(math.ceil(len(outfit_buttons) / 2))]
    for row in outfit_rows:
        choose_outfit_menu.inline_keyboard.insert(-1, row)
    return choose_outfit_menu


buy_outfit_menu = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Купить",
                callback_data=choose_item_callback.new(
                    item_type="outfit",
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
