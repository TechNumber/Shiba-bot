from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# TODO: не выводить кнопку, если соответствующих предметов нет в инвентаре
from keyboards.inline.callback_datas import show_inventory_items_callback, cancel_callback


async def get_home_inventory_menu(user_id: int):
    """
    Данный обработчик формирует и возвращает меню с кнопками "Оружие", "Одежда",
    "Еда", "Отмена", при помощи которого пользователь выбирает категорию предметов
    в инвентаре, которые хочет посмотреть.

    Args:
        user_id (int): id пользователя; оно помещается в CallbackData каждой кнопки
        для последующей проверки фильтром IsCalledByOwner(). Благодаря этому
        нажатие других пользователей на кнопки, предназначенные для данного пользователя,
        не будут обрабатываться.

    Returns:
        (InlineKeyboardMarkup): Меню выбора категории предметов инвентаря

    """
    home_inventory_menu = InlineKeyboardMarkup(
        row_width=3,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Оружие",
                    callback_data=show_inventory_items_callback.new(
                        user_id=user_id,
                        item_type="weapon"
                    )
                ),
                InlineKeyboardButton(
                    text="Одежда",
                    callback_data=show_inventory_items_callback.new(
                        user_id=user_id,
                        item_type="outfit"
                    )
                ),
                InlineKeyboardButton(
                    text="Еда",
                    callback_data=show_inventory_items_callback.new(
                        user_id=user_id,
                        item_type="meal"
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text="Отмена",
                    callback_data=cancel_callback.new(
                        user_id=user_id,
                        cancel_type="inventory"
                    )
                )
            ]
        ]
    )
    return home_inventory_menu
