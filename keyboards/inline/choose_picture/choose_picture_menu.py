from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import choose_picture_callback, cancel_callback


async def get_choose_picture_menu(user_id: int,
                                  picture: str):
    choose_picture_menu = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Выбрать",
                    callback_data=choose_picture_callback.new(
                        user_id=user_id,
                        picture_path=picture
                    )
                ),
                InlineKeyboardButton(
                    text="Сменить",
                    callback_data=cancel_callback.new(
                        user_id=user_id,
                        cancel_type="picture"
                    )
                )
            ]
        ]
    )
    return choose_picture_menu
