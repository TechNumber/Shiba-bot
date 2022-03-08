from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.utils.markdown import hcode

from loader import dp
from utils.db_api import user_commands as commands


@dp.message_handler(Command("email"))
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer("Пришли мне свой email в ответ на это сообщение")
    await state.set_state("email")


@dp.message_handler(state="email")
async def enter_email(message: types.Message, state: FSMContext):
    email = message.text
    await commands.update_user_email(email=email, user_id=message.from_user.id)
    user = await commands.select_user(user_id=message.from_user.id)
    await message.answer("Данные обновлены. Запись в БД: \n" +
                         hcode(f"user_id={user.user_id}\n"
                               f"user_name={user.user_name}\n"
                               f"shibu_name={user.shibu_name}"))
    await state.finish()
