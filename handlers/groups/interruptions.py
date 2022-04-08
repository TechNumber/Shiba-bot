from aiogram import types
from aiogram.dispatcher.filters import StateFilter

from loader import dp
from states.game_state import GameState
from states.register_state import RegisterState


@dp.message_handler(state=GameState.shopping)
async def in_shop(message: types.Message):
    await message.answer("Ваша собака не может выполнять никаких действий, пока шиба находится в магазине!")
