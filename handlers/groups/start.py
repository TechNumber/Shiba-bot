from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from states.game_state import GameState
from states.register_state import RegisterState
from utils.db_api import user_commands as commands


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
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
