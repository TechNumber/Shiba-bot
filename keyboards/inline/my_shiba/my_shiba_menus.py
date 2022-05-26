from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import call_service_callback


async def get_my_shiba_menu(user_id: int):
    my_shiba_menu = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Инвентарь",
                    callback_data=call_service_callback.new(
                        user_id=user_id,
                        service_type="inventory"
                    )
                ),
                InlineKeyboardButton(
                    text="Магазин",
                    callback_data=call_service_callback.new(
                        user_id=user_id,
                        service_type="shop"
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text="Сразиться с монстром подземелья",
                    callback_data=call_service_callback.new(
                        user_id=user_id,
                        service_type="mob_fight"
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text="Переименовать шибу",
                    callback_data=call_service_callback.new(
                        user_id=user_id,
                        service_type="shiba_rename"
                    )
                )
            ]
        ]
    )
    return my_shiba_menu