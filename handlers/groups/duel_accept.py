from aiogram import types
from aiogram.dispatcher.filters import Command, StateFilter

from states.game_state import GameState
from utils.db_api import user_commands, duel_commands, effect_commands
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
    msg += "Чтобы отклонить вызов на дуэль, введите команду:\n '/decline @имя_пользователя'."
    await message.answer(msg, disable_web_page_preview=True)


@dp.message_handler(Command("accept"), state=GameState.registered)
async def duel_accept(message: types.message):
    sender_id = (await user_commands.select_user(message.from_user.id)).user_id
    sender = await user_commands.select_user(sender_id)
    requesters_id_list = await duel_commands.select_all_senders_id(sender_id)
    duelist = None
    duelist_name = None
    blocks = dict(message).get("text").split(" ")
    if len(blocks) > 1 and "@" in blocks[1]:
        for i in range(len(requesters_id_list)):
            duelist = (await dp.bot.get_chat_member(
                user_id=requesters_id_list[i],
                chat_id=requesters_id_list[i])).user
            if duelist.mention == dict(message).get("text").split(" ")[1]:
                duelist_name = duelist.username
            break
        if duelist_name is None:
            await message.answer("Этот пользователь не вызывал Вас на дуэль!", disable_web_page_preview=True)
            return 0
        log = f"Вызов от пользователя {duelist_name} был принят!\n"
        duelist_u = await user_commands.select_user(duelist.id)
        cur_exp1 = sender.exp
        cur_money1 = sender.money
        cur_exp2 = duelist_u.exp
        cur_money2 = duelist_u.money
        log += await user_commands.combat_sequence(sender_id, duelist.id)
        sender_n = await user_commands.select_user(sender_id)
        duelist_n = await user_commands.select_user(duelist.id)
        shiba1 = str(sender_n.shiba_name)
        shiba2 = str(duelist_n.shiba_name)
        if cur_exp1 != sender_n.exp:
            log += f"Получено опыта шибой {shiba1}: {sender_n.exp - cur_exp1} \n"
        if cur_exp2 != duelist_n.exp:
            log += f"Получено опыта шибой {shiba2}: {duelist_n.exp - cur_exp2} \n"
        if cur_money1 != sender_n.money:
            log += f"Получено денег шибой {shiba1}: {sender_n.money - cur_money1} \n"
        if cur_money2 != duelist_n.money:
            log += f"Получено денег шибой {shiba2}: {duelist_n.money - cur_money2} \n"
        lvup1 = await user_commands.check_level_up(sender_id)
        if lvup1 != 0:
            log += f"Уровень шибы {shiba1} повышен!\n Получено очков улучшений характеристик: {lvup1}"
            await sender_n.update(level_up=sender_n.level_up + lvup1).apply()
        lvup2 = await user_commands.check_level_up(duelist.id)
        if lvup2 != 0:
            log += f"Уровень шибы {shiba2} повышен!\n Получено очков улучшений характеристик: {lvup2}"
            await sender_n.update(level_up=duelist_n.level_up + lvup2).apply()
        ko1 = await user_commands.check_knockout(sender_id)
        if ko1:
            log += f"Шиба {shiba1} потерпела поражение! Весь опыт, накопленный на данном уровне, потерян."
        ko2 = await user_commands.check_knockout(duelist.id)
        if ko2:
            log += f"Шиба {shiba2} потерпела поражение! Весь опыт, накопленный на данном уровне, потерян."
        await effect_commands.reduce_duration(sender_id)
        await effect_commands.reduce_duration(duelist.id)
        await duel_commands.delete_duel(duelist.id, sender_id)
        await message.answer(log, disable_web_page_preview=True)
    elif len(blocks) > 1 and "tg://user?id=" in blocks[1]:
        id_from_message = int(blocks[1][blocks[1].index("tg://user?id=") +
                                        len("tg://user?id="):
                                        blocks[1].index(")")])
        duelist = (await dp.bot.get_chat_member(
            user_id=id_from_message,
            chat_id=id_from_message)).user
        duelist_name = (await dp.bot.get_chat_member(
            user_id=id_from_message,
            chat_id=id_from_message)).user.full_name
        if duelist_name is None:
            await message.answer("Этот пользователь не вызывал Вас на дуэль!", disable_web_page_preview=True)
            return 0
        log = f"Вызов от пользователя {duelist_name} был принят!\n"
        duelist_u = await user_commands.select_user(duelist.id)
        cur_exp1 = sender.exp
        cur_money1 = sender.money
        cur_exp2 = duelist_u.exp
        cur_money2 = duelist_u.money
        log += await user_commands.combat_sequence(sender_id, duelist.id)
        sender_n = await user_commands.select_user(sender_id)
        duelist_n = await user_commands.select_user(duelist.id)
        shiba1 = str(sender_n.shiba_name)
        shiba2 = str(duelist_n.shiba_name)
        if cur_exp1 != sender_n.exp:
            log += f"Получено опыта шибой {shiba1}: {sender_n.exp - cur_exp1} \n"
        if cur_exp2 != duelist_n.exp:
            log += f"Получено опыта шибой {shiba2}: {duelist_n.exp - cur_exp2} \n"
        if cur_money1 != sender_n.money:
            log += f"Получено денег шибой {shiba1}: {sender_n.money - cur_money1} \n"
        if cur_money2 != duelist_n.money:
            log += f"Получено денег шибой {shiba2}: {duelist_n.money - cur_money2} \n"
        lvup1 = await user_commands.check_level_up(sender_id)
        if lvup1 != 0:
            log += f"Уровень шибы {shiba1} повышен!\n Получено очков улучшений характеристик: {lvup1}"
            await sender_n.update(level_up=sender_n.level_up + lvup1).apply()
        lvup2 = await user_commands.check_level_up(duelist.id)
        if lvup2 != 0:
            log += f"Уровень шибы {shiba2} повышен!\n Получено очков улучшений характеристик: {lvup2}"
            await sender_n.update(level_up=duelist_n.level_up + lvup2).apply()
        ko1 = await user_commands.check_knockout(sender_id)
        if ko1:
            log += f"Шиба {shiba1} потерпела поражение! Весь опыт, накопленный на данном уровне, потерян."
        ko2 = await user_commands.check_knockout(duelist.id)
        if ko2:
            log += f"Шиба {shiba2} потерпела поражение! Весь опыт, накопленный на данном уровне, потерян."
        await effect_commands.reduce_duration(sender_id)
        await effect_commands.reduce_duration(duelist.id)
        await duel_commands.delete_duel(duelist.id, sender_id)
        await message.answer(log, disable_web_page_preview=True)
    else:
        await message.answer("Вы неверно указали пользователя!")


@dp.message_handler(Command("decline"), state=GameState.registered)
async def duel_decline(message: types.message):
    sender_id = (await user_commands.select_user(message.from_user.id)).user_id
    requesters_id_list = await duel_commands.select_all_senders_id(sender_id)
    duelist = None
    duelist_name = None
    blocks = dict(message).get("text").split(" ")
    if len(blocks) > 1 and "@" in blocks[1]:
        for i in range(len(requesters_id_list)):
            duelist = (await dp.bot.get_chat_member(
                user_id=requesters_id_list[i],
                chat_id=requesters_id_list[i])).user
            if duelist.mention == dict(message).get("text").split(" ")[1]:
                duelist_name = duelist.username
            break
        if duelist_name is None:
            await message.answer("Этот пользователь не вызывал Вас на дуэль!", disable_web_page_preview=True)
            return 0
        log = f"Вызов от пользователя {duelist_name} был отклонен.\n"
        await duel_commands.delete_duel(duelist.id, sender_id)
        await message.answer(log, disable_web_page_preview=True)
    elif len(blocks) > 1 and "tg://user?id=" in blocks[1]:
        id_from_message = int(blocks[1][blocks[1].index("tg://user?id=") +
                                        len("tg://user?id="):
                                        blocks[1].index(")")])
        duelist = (await dp.bot.get_chat_member(
            user_id=id_from_message,
            chat_id=id_from_message)).user
        duelist_name = (await dp.bot.get_chat_member(
            user_id=id_from_message,
            chat_id=id_from_message)).user.full_name
        if duelist_name is None:
            await message.answer("Этот пользователь не вызывал Вас на дуэль!", disable_web_page_preview=True)
            return 0
        log = f"Вызов от пользователя {duelist_name} был отклонен.\n"
        await duel_commands.delete_duel(duelist.id, sender_id)
        await message.answer(log, disable_web_page_preview=True)
    else:
        await message.answer("Вы неверно указали пользователя!")