import math

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import cancel_callback, show_shop_items_callback, show_item_callback, \
    buy_item_callback
from utils.db_api import outfit_commands


async def get_shop_all_outfits_menu(user_id: int):
    shop_outfits_menu = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Оружие",
                    callback_data=cancel_callback.new(
                        user_id=user_id,
                        cancel_type="buy"
                    )
                ),
                InlineKeyboardButton(
                    text="Отмена",
                    callback_data=cancel_callback.new(
                        user_id=user_id,
                        cancel_type="shop"
                    )
                ),
                InlineKeyboardButton(
                    text="Еда",
                    callback_data=show_shop_items_callback.new(
                        user_id=user_id,
                        item_type="meal"
                    )
                )
            ]
        ],
        resize_keyboard=True
    )
    outfits = await outfit_commands.select_all_outfits()
    outfit_buttons = [InlineKeyboardButton(
        text=outfit.outfit_name,
        callback_data=show_item_callback.new(
            user_id=user_id,
            item_type="outfit",
            item_id=outfit.outfit_id
        )
    ) for outfit in outfits]
    outfit_rows = [outfit_buttons[i * 2:i * 2 + 2] for i in range(math.ceil(len(outfit_buttons) / 2))]
    for row in outfit_rows:
        shop_outfits_menu.inline_keyboard.insert(-1, row)
    return shop_outfits_menu


async def get_shop_outfit_menu(user_id: int, outfit_id: int):
    outfit_menu = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Купить",
                    callback_data=buy_item_callback.new(
                        user_id=user_id,
                        item_type="outfit",
                        item_id=outfit_id
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
    return outfit_menu
