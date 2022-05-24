import random

import gino
from aiogram import types
from aiogram.dispatcher.filters import Command, StateFilter
from sqlalchemy import or_

from states.game_state import GameState
from utils.db_api import user_commands, mob_commands
from loader import dp, bot
from utils.db_api.schemas.mob import Mob


@dp.message_handler(Command("fight_mob"), state=GameState.registered)
async def fight_mob(message: types.message):
    sender_id = (await user_commands.select_user(message.from_user.id)).user_id
    sender = await user_commands.select_user(sender_id)
    user_lvl = sender.level
    mob_ids = await Mob.query.where(
        or_(
            Mob.mob_level > user_lvl - 5,
            Mob.mob_level < user_lvl + 5
        )
    ).gino.load(Mob.mob_id).all()
    cur_exp = sender.exp
    if len(mob_ids) == 0:
        mob_ids = await Mob.query.gino.load(Mob.mob_id).all()
    log = await user_commands.mob_combat(sender_id, mob_ids[random.randint(0, len(mob_ids))-1])
    sender_n = await user_commands.select_user(sender_id)
    if cur_exp != sender_n.exp:
        log += f"Получено опыта: {sender_n.exp - cur_exp} \n"
    lvup = await user_commands.check_level_up(sender_id)
    if lvup != 0:
        log += f"Уровень повышен!\n Получено очков улучшений характеристик: {lvup}"
        await sender_n.update(level_up=sender_n.level_up + lvup).apply()
    ko = await user_commands.check_knockout(sender_id)
    if ko:
        log += "Шиба потерпела поражение! Весь опыт, накопленный на данном уровне, потерян."
    await message.answer(log, disable_web_page_preview=True)
