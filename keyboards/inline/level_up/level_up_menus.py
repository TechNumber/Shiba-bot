from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import apply_level_up_callback, cancel_callback, level_attribute_up_callback
from utils.db_api.schemas.user import User


async def get_level_up_menu(user: User,
                            max_health_added_points: int,
                            strength_added_points: int,
                            agility_added_points: int):
    level_up_menu = InlineKeyboardMarkup(
        row_width=3,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Здоровье: {user.max_health}. Очков добавлено: {max_health_added_points}",
                    callback_data=level_attribute_up_callback.new(
                        user_id=user.user_id,
                        attribute_type="max_health"
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"Сила: {user.strength}. Очков добавлено: {strength_added_points}",
                    callback_data=level_attribute_up_callback.new(
                        user_id=user.user_id,
                        attribute_type="strength"
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"Ловкость: {user.agility}. Очков добавлено: {agility_added_points}",
                    callback_data=level_attribute_up_callback.new(
                        user_id=user.user_id,
                        attribute_type="agility"
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text="Применить",
                    callback_data=apply_level_up_callback.new(
                        user_id=user.user_id
                    )
                ),
                InlineKeyboardButton(
                    text="Отмена",
                    callback_data=cancel_callback.new(
                        user_id=user.user_id,
                        cancel_type="level_up"
                    )
                )
            ]

        ]
    )
    return level_up_menu
