from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from filters.is_chat import IsChat
from loader import dp


@dp.message_handler(CommandStart(), IsChat())
async def bot_start_not_registered(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}!\nДанный игровой бот предназначен для групповых "
        f"чатов. Чтобы запустить игру, добавь бота в чат и отправь команду /start. Чтобы ознакомиться "
        f"с правилами игры, отправь команду /help."
    )
