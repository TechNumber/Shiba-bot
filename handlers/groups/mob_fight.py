import random

import gino
from aiogram import types
from aiogram.dispatcher.filters import Command, StateFilter
from sqlalchemy import or_, and_

from filters import IsCalledByOwner
from keyboards.inline.callback_datas import call_service_callback
from states.game_state import GameState
from utils.db_api import user_commands, mob_commands, effect_commands
from loader import dp, bot
from utils.db_api.db_gino import db
from utils.db_api.schemas.mob import Mob


@dp.message_handler(Command("fight_mob"), state=GameState.registered)
async def fight_mob(message: types.message):
    sender_id = (await user_commands.select_user(message.from_user.id)).user_id
    sender = await user_commands.select_user(sender_id)
    user_lvl = sender.level
    mob_ids = await Mob.query.where(
        and_(
            Mob.mob_level > user_lvl - 5,
            Mob.mob_level < user_lvl + 5
        )
    ).gino.load(Mob.mob_id).all()
    cur_exp = sender.exp
    cur_money = sender.money
    if len(mob_ids) == 0:
        mob_ids = await Mob.query.gino.load(Mob.mob_id).all()
    log = await user_commands.mob_combat(sender_id, mob_ids[random.randint(0, len(mob_ids)) - 1])
    sender_n = await user_commands.select_user(sender_id)
    if cur_exp != sender_n.exp:
        log += f"Получено опыта: {sender_n.exp - cur_exp} \n"
    if cur_money != sender_n.money:
        log += f"Получено денег: {sender_n.money - cur_money} \n"
    lvup = await user_commands.check_level_up(sender_id)
    if lvup != 0:
        log += f"Уровень повышен!\n Получено очков улучшений характеристик: {lvup}"
        await sender_n.update(level_up=sender_n.level_up + lvup).apply()
    ko = await user_commands.check_knockout(sender_id)
    if ko:
        log += "Шиба потерпела поражение! Весь опыт, накопленный на данном уровне, потерян."
    await effect_commands.reduce_duration(sender_id)
    await message.answer(log, disable_web_page_preview=True)


@dp.callback_query_handler(IsCalledByOwner(), call_service_callback.filter(service_type="mob_fight"),
                           state=GameState.registered)
async def fight_mob_from_callback(call: types.CallbackQuery):
    sender_id = (await user_commands.select_user(call.from_user.id)).user_id
    sender = await user_commands.select_user(sender_id)
    user_lvl = sender.level
    mob_ids = await Mob.query.where(
        and_(
            Mob.mob_level > user_lvl - 5,
            Mob.mob_level < user_lvl + 5
        )
    ).gino.load(Mob.mob_id).all()
    cur_exp = sender.exp
    cur_money = sender.money
    if len(mob_ids) == 0:
        mob_ids = await Mob.query.gino.load(Mob.mob_id).all()
    log = await user_commands.mob_combat(sender_id, mob_ids[random.randint(0, len(mob_ids)) - 1])
    sender_n = await user_commands.select_user(sender_id)
    if cur_exp != sender_n.exp:
        log += f"Получено опыта: {sender_n.exp - cur_exp} \n"
    if cur_money != sender_n.money:
        log += f"Получено денег: {sender_n.money - cur_money} \n"
    lvup = await user_commands.check_level_up(sender_id)
    if lvup != 0:
        log += f"Уровень повышен!\n Получено очков улучшений характеристик: {lvup}"
        await sender_n.update(level_up=sender_n.level_up + lvup).apply()
    ko = await user_commands.check_knockout(sender_id)
    if ko:
        log += "Шиба потерпела поражение! Весь опыт, накопленный на данном уровне, потерян."
    await effect_commands.reduce_duration(sender_id)
    await call.message.answer(log, disable_web_page_preview=True)
