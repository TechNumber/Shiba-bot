import os
import pathlib
import random
import shutil

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp
from aiogram.types import InputFile, InputMedia, InputMediaPhoto

from filters import IsCalledByOwner
from handlers.groups.help import bot_help
from handlers.groups.update_db import shiba_rename_from_callback
from keyboards.inline.callback_datas import choose_picture_callback, cancel_callback
from keyboards.inline.choose_picture.choose_picture_menu import get_choose_picture_menu
from loader import dp
from states.game_state import GameState
from utils.db_api import user_commands as commands, user_commands


@dp.message_handler(CommandStart(), state=GameState.registered)
async def bot_start_registered(message: types.Message):
    await message.answer("Ты уже зарегистрирован в игре!")


@dp.message_handler(CommandStart())
async def bot_start_not_registered(message: types.Message):
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

    # await message.answer(
    #     "\n".join(
    #         [
    #             f'Привет, {message.from_user.full_name}!',
    #             f'Ты был занесён в базу',
    #             f'В базе <b>{count}</b> пользователей',
    #         ]
    #     )
    # )
    if message.from_user.username is not None:
        sender_link = f"<a href=\"t.me/{message.from_user.username}\">{message.from_user.username}</a>"
    else:
        sender_link = f"<a href=\"tg://user?id={message.from_user.id}\">{message.from_user.full_name}</a>"
    await message.answer(
        f"Приветствую в игре, {sender_link}!\n\n"
        f"Здесь начинается твой путь воина. Тебе предстоит играть за отважную собаку породы шиба-ину, "
        f"скитающуюся по деревням и префектурам острова Хонсю в поисках гармонии и воинского мастерства.\n\n"
        f"<b>Удачного странствия!</b>",
        disable_web_page_preview=True
    )
    await bot_help(message)
    if len(os.listdir(pathlib.Path(__file__).parent / "../../user_pictures/unused")) > 0:
        picture = random.choice(os.listdir(pathlib.Path(__file__).parent / "../../user_pictures/unused"))
        await GameState.choosing_picture.set()
        await dp.bot.send_photo(
            message.chat.id,
            InputFile(path_or_bytesio=pathlib.Path(__file__).parent / "../../user_pictures/unused/" / picture),
            f"Перед тем, как продолжить, выбери свою шибу. "
            f"Выбирай тщательно: её нельзя будет сменить впоследствии!",
            reply_markup=await get_choose_picture_menu(message.from_user.id, picture)
        )
    else:
        await GameState.registered.set()


@dp.callback_query_handler(IsCalledByOwner(), choose_picture_callback.filter(),
                           state=GameState.choosing_picture)
async def choose_picture(call: types.CallbackQuery):
    user = await user_commands.select_user(user_id=call.from_user.id)
    picture = (call.data.split(":"))[-1]
    await user.update(pic_path=picture).apply()
    shutil.move(pathlib.Path(__file__).parent / "../../user_pictures/unused" / picture,
                pathlib.Path(__file__).parent / "../../user_pictures/used" / picture)
    await call.message.edit_caption("Шиба успешно выбрана!", reply_markup=None)
    await shiba_rename_from_callback(call)


@dp.callback_query_handler(IsCalledByOwner(), cancel_callback.filter(cancel_type="picture"),
                           state=GameState.choosing_picture)
async def change_picture(call: types.CallbackQuery):
    picture = random.choice(os.listdir(pathlib.Path(__file__).parent / "../../user_pictures/unused"))
    input_media_photo = InputMediaPhoto(
        InputFile(path_or_bytesio=pathlib.Path(__file__).parent / "../../user_pictures/unused/" / picture))
    await call.message.edit_media(
        input_media_photo
    )
    await call.message.edit_caption(
        f"Перед тем, как продолжить, выбери свою шибу. "
        f"Выбирай тщательно: её нельзя будет сменить впоследствии!",
        reply_markup=await get_choose_picture_menu(call.from_user.id, picture)
    )
