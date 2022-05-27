from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp

from handlers.groups.help import bot_help
from loader import dp
from states.game_state import GameState
from utils.db_api import user_commands as commands


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
    await GameState.registered.set()
