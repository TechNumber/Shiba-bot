from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.utils.markdown import hcode

from loader import dp
from utils.db_api import user_commands as commands


@dp.message_handler(Command("shiba_rename"))
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer("Пришли мне новое имя пса в ответ на это сообщение")
    await state.set_state("shiba_rename")


@dp.message_handler(state="shiba_rename")
async def enter_email(message: types.Message, state: FSMContext):
    shiba_name = message.text
    await commands.update_shiba_name(shiba_name=shiba_name, user_id=message.from_user.id)
    user = await commands.select_user(user_id=message.from_user.id)
    await message.answer("Данные обновлены. Запись в БД: \n" +
                         hcode(f"user_id={user.user_id}\n"
                               f"user_name={user.user_name}\n"
                               f"shiba_name={user.shiba_name}"))
    await state.finish()
