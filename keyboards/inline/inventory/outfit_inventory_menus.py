import math

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import discard_item_callback, cancel_callback, \
    equip_item_callback, show_item_callback
from utils.db_api import inventory_outfit_commands


async def get_inventory_all_outfits_menu(user_id: int):
    inventory_outfits_menu = InlineKeyboardMarkup(
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
    outfits = await inventory_outfit_commands.select_all_outfits_by_user_id(user_id=user_id)
    outfit_buttons = [InlineKeyboardButton(
        text="{}, {} шт.".format(
            outfit.outfit_name,
            await inventory_outfit_commands.get_outfit_amount(user_id=user_id, outfit_id=outfit.outfit_id)
        ),
        callback_data=show_item_callback.new(
            user_id=user_id,
            item_type="outfit",
            item_id=outfit.outfit_id
        )
    ) for outfit in outfits]
    outfit_rows = [outfit_buttons[i * 2:i * 2 + 2] for i in range(math.ceil(len(outfit_buttons) / 2))]
    for row in outfit_rows:
        inventory_outfits_menu.inline_keyboard.insert(-1, row)
    return inventory_outfits_menu


async def get_inventory_outfit_menu(user_id: int, outfit_id: int):
    equip_outfit_menu = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Надеть",
                    callback_data=equip_item_callback.new(
                        user_id=user_id,
                        item_type="outfit",
                        item_id=outfit_id
                    )
                ),
                InlineKeyboardButton(
                    text="Выбросить",
                    callback_data=discard_item_callback.new(
                        user_id=user_id,
                        item_type="outfit",
                        item_id=outfit_id
                    )
                ),
                InlineKeyboardButton(
                    text="Отмена",
                    callback_data=cancel_callback.new(
                        user_id=user_id,
                        cancel_type="equip_outfit"
                    )
                )
            ],
        ],
        resize_keyboard=True
    )
    return equip_outfit_menu

# TODO: пометка "(Выбрано)", если предмет уже выбран
