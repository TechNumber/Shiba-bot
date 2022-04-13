from aiogram import types
from aiogram.dispatcher.filters import StateFilter

from loader import dp
from states.game_state import GameState


@dp.message_handler(state=GameState.shopping)
async def in_shop(message: types.Message):
    """
    Данный обработчик уведомляет пользователя, что он не может совершать никаких действий,
    пока тот находится в магазине

    Filters:
        state=GameState.shopping: пользователь находится в состоянии, отвечающем за нахождение
        в магазине

    Args:
        message (types.Message): любое сообщение с обращением к боту, вызванное во время
        нахождения в магазине

    Returns:
        None
    """
    await message.answer("Ваша собака не может выполнять никаких действий, пока шиба находится в магазине!")
