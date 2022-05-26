from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from filters import IsCalledByOwner
from handlers.groups import shop, inventory, mob_fight, update_db
from keyboards.inline.callback_datas import call_service_callback
from keyboards.inline.my_shiba.my_shiba_menus import get_my_shiba_menu
from loader import dp
from states.game_state import GameState
from utils.db_api import user_commands


@dp.message_handler(Command("my_shiba"), state=GameState.registered)
async def show_my_shiba_menu(message: types.Message):
    if message.from_user.username is not None:
        sender_link = f"<a href=\"t.me/{message.from_user.username}\">{message.from_user.username}</a>"
    else:
        sender_link = f"<a href=\"tg://user?id={message.from_user.id}\">{message.from_user.full_name}</a>"
    user = await user_commands.select_user(message.from_user.id)
    await message.answer(
        f"Информация о шибе игрока {sender_link}:"
        f"\n\U0001F415 Имя шибы: {user.shiba_name}"
        f"\n\U0001F31F Уровень шибы: {user.level}"
        f"\n\U00002728 Очков опыта: {user.exp}"
        f"\n\U00002B06 Очков улучшений: {user.level_up}"
        f"\n\U00002764 Здоровье шибы: {user.health}/{user.max_health}"
        f"\n\U0001F4AA Сила шибы: {user.strength}"
        f"\n\U0001F977 Ловкость шибы: {user.agility}"
        f"\n\U0001F4B4 Денег: {user.money}",
        reply_markup=await get_my_shiba_menu(user_id = message.from_user.id),
        disable_web_page_preview=True
        # TODO: посмотреть инвентарь, магазин и т.д.
    )

"""
🐸Имя жабы: Ахматова
⭐Уровень вашей жабы: 35
🍰Сытость: 39/45
👑Статус жабы: prime
❤Состояние: 🐸 Живая
🐞Букашки: 19543
⚒Класс: Отсутствует
👻Настроение: Отличное (480)
"""
