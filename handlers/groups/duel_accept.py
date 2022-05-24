from aiogram import types
from aiogram.dispatcher.filters import Command, StateFilter

from states.game_state import GameState
from utils.db_api import user_commands, duel_commands
from loader import dp, bot

'''
@dp.message_handler(Command("add_dummies"), state=GameState.registered)
async def add_dummies(message: types.message):
    sender_id = (await user_commands.select_user(message.from_user.id)).user_id
    for i in range(10):
        await user_commands.add_user(user_id=i, user_name=f"Болванчик {i}", shiba_name=f"Шиба {i}")
        await duel_commands.add_duel(i, sender_id)
    await message.answer("Болванчики добавлены!", disable_web_page_preview=True) 
'''


@dp.message_handler(Command("duel_list"), state=GameState.registered)
async def print_duel_list(message: types.message):
    if message.from_user.username is not None:
        sender_link = f"<a href=\"t.me/{message.from_user.username}\">{message.from_user.username}</a>"
    else:
        sender_link = f"<a href=\"tg://user?id={message.from_user.id}\">{message.from_user.full_name}</a>"
    sender_id = (await user_commands.select_user(message.from_user.id)).user_id
    sender_shiba_name = (await user_commands.select_user(message.from_user.id)).shiba_name
    sender_ids = await duel_commands.select_all_senders_id(sender_id)
    duel_sender_users: str = ""
    if len(sender_ids) == 0:
        await message.answer("Никто не вызывал Вас на дуэль.")
        return 0
    msg = f"Список вызовов на дуэль, адресованных шибе {sender_shiba_name} пользователя {sender_link}:\n"
    for id in sender_ids:
        duelist_user = await user_commands.select_user(id)
        duelist_name = duelist_user.user_name
        duelist_shiba = duelist_user.shiba_name
        duel_sender_users += f" - {duelist_shiba} (Хозяин: {duelist_name})\n"
    msg += duel_sender_users
    msg += "Чтобы принять вызов на дуэль, введите команду:\n '/accept @имя_пользователя'."
    await message.answer(msg, disable_web_page_preview=True)

