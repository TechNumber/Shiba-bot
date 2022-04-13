from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command, StateFilter
from aiogram.utils.markdown import hcode

from loader import dp
from states.game_state import GameState
from utils.db_api import user_commands as commands


@dp.message_handler(Command("shiba_rename"), state=GameState.registered)
async def shiba_rename(message: types.Message):
    """
    Вводит игрока в режим переименования собаки.

    Filters:
        Command("shiba_rename"): Сообщение содержит команду /shiba_rename
        state=GameState.registered: Пользователь, вызвавший команду, участвует в игре

    Args:
        message (types.Message): Сообщение с командой /shiba_rename

    Returns:
        None
    """

    await message.answer("Пришли мне новое имя пса в ответ на это сообщение")
    await GameState.naming.set()


@dp.message_handler(state=GameState.naming)
async def enter_shiba_name(message: types.Message):
    """
    Заменяет имя собаки пользователя на то, которое он прислал в ответ на сообщение
    о переименовании.

    Filters:
        state=GameState.naming: Пользователь, приславший имя, находился в состоянии
        именования

    Args:
        message (types.Message): Сообщение с новым именем собаки

    Returns:
        None
    """
    shiba_name = message.text
    await commands.update_shiba_name(shiba_name=shiba_name, user_id=message.from_user.id)
    user = await commands.select_user(user_id=message.from_user.id)
    await message.answer("Данные обновлены. Запись в БД: \n" +
                         hcode(f"user_id={user.user_id}\n"
                               f"user_name={user.user_name}\n"
                               f"shiba_name={user.shiba_name}"))
    await GameState.registered.set()
