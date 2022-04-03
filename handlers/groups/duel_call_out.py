from aiogram import types
from aiogram.dispatcher.filters import Command

from utils.db_api import user_commands
from loader import dp, bot


@dp.message_handler(Command("duel"))
async def duel_call_out(message: types.Message):
    user_id_list = await user_commands.get_all_users_id()
    blocks = message.md_text.strip().split()
    if message.from_user.username is not None:
        sender_link = f"<a href=\"t.me/{message.from_user.username}\">{message.from_user.username}</a>"
    else:
        sender_link = f"<a href=\"tg://user?id={message.from_user.id}\">{message.from_user.full_name}</a>"
    sender_shiba_name = (await user_commands.select_user(message.from_user.id)).shiba_name
    if len(blocks) > 1 and "@" in blocks[1]:
        message_mention = blocks[1]
        i = 0
        user_mention = (await dp.bot.get_chat_member(
            user_id=user_id_list[i],
            chat_id=user_id_list[i])).user.mention
        while i < len(user_id_list) and message_mention != user_mention:
            user_mention = (await dp.bot.get_chat_member(
                user_id=user_id_list[i],
                chat_id=user_id_list[i])).user.mention
            i += 1
        if user_mention != message_mention:
            await message.answer("Вы не можете вызвать на бой пользователя без шибы!")
        else:
            await message.answer(
                f"{user_mention}, ты был вызван на дуэль шибой {sender_shiba_name} пользователя {sender_link}! Ты можешь принять или отклонить вызов на дуэль, нажав на кнопку \"Дуэли\" в меню шибы.",
                disable_web_page_preview=True)
    elif len(blocks) > 1 and "tg://user?id=" in blocks[1]:
        id_from_message = int(blocks[1][blocks[1].index("tg://user?id=") +
                                        len("tg://user?id="):
                                        blocks[1].index(")")])
        if id_from_message not in user_id_list:
            await message.answer("Вы не можете вызвать на бой пользователя без шибы!")
        else:
            receiver_name = (await dp.bot.get_chat_member(
                user_id=id_from_message,
                chat_id=id_from_message)).user.full_name
            await message.answer(
                f"<a href=\"tg://user?id={id_from_message}\">{receiver_name}</a>, ты был вызван на дуэль шибой {sender_shiba_name} пользователя {sender_link}! Ты можешь принять или отклонить вызов на дуэль, нажав на кнопку \"Дуэли\" в меню шибы.",
                disable_web_page_preview=True)
    else:
        await message.answer("Вы неверно указали пользователя, с которым хотите драться!")
