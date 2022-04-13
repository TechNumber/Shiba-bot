from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from states.game_state import GameState
from utils.db_api import user_commands as commands


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    """
    Данный обработчик вносит пользователя в таблицу пользователей, участвующих в
    игре, и присваивает ему статус "Зарегистрирован".

    Filters:
        CommandStart(): Сообщение содержит команду /start

    Args:
        message (types.Message): Сообщение с командой /start

    Returns:
        None
    """
    user_name = message.from_user.full_name
    await commands.add_user(user_id=message.from_user.id,
                            user_name=user_name)

    count = await commands.count_users()
    await message.answer(
        "\n".join(
            [
                f'Привет, {message.from_user.full_name}!',
                f'Ты был занесён в базу',
                f'В базе <b>{count}</b> пользователей',
            ]
        )
    )
    await GameState.registered.set()
