import math

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import buy_item_callback, discard_item_callback, cancel_callback, \
    equip_item_callback, show_item_callback
from utils.db_api import weapon_commands, inventory_weapon_commands
from utils.db_api.inventory_weapon_commands import get_weapon_amount


async def get_inventory_all_weapons_menu(user_id: int):
    inventory_weapon_menu = InlineKeyboardMarkup(
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
    weapons = await inventory_weapon_commands.select_all_weapons_by_user_id(user_id=user_id)
    weapon_buttons = [InlineKeyboardButton(
        text="{}, {} шт.".format(
            weapon.weapon_name,
            await get_weapon_amount(user_id=user_id, weapon_id=weapon.weapon_id)
        ),
        callback_data=show_item_callback.new(
            user_id=user_id,
            item_type="weapon",
            item_id=weapon.weapon_id
        )
    ) for weapon in weapons]
    weapon_rows = [weapon_buttons[i * 2:i * 2 + 2] for i in range(math.ceil(len(weapon_buttons) / 2))]
    for row in weapon_rows:
        inventory_weapon_menu.inline_keyboard.insert(-1, row)
    return inventory_weapon_menu


async def get_inventory_weapon_menu(user_id: int, weapon_id: int):
    equip_weapon_menu = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Экипировать",
                    callback_data=equip_item_callback.new(
                        user_id=user_id,
                        item_type="weapon",
                        item_id=weapon_id
                    )
                ),
                InlineKeyboardButton(
                    text="Выбросить",
                    callback_data=discard_item_callback.new(
                        user_id=user_id,
                        item_type="weapon",
                        item_id=weapon_id
                    )
                ),
                InlineKeyboardButton(
                    text="Отмена",
                    callback_data=cancel_callback.new(
                        user_id=user_id,
                        cancel_type="equip"
                    )
                )
            ],
        ],
        resize_keyboard=True
    )
    return equip_weapon_menu

# TODO: пометка "(Выбрано)", если предмет уже выбран
