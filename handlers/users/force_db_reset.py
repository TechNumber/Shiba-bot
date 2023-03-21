from aiogram import types
from aiogram.dispatcher.filters import Command
from asyncpg import UndefinedTableError

from data import config
from filters.is_admin import IsAdmin
from loader import dp
from states.game_state import GameState
from utils.db_api import all_init
from utils.db_api.db_gino import db
from utils.db_api.schemas.duel import Duel
from utils.db_api.schemas.effect import Effect
from utils.db_api.schemas.inventory_meal import InventoryMeal
from utils.db_api.schemas.inventory_outfit import InventoryOutfit
from utils.db_api.schemas.inventory_weapon import InventoryWeapon
from utils.db_api.schemas.user import User


@dp.message_handler(Command("force_db_reset"), IsAdmin(), state="*")
async def force_db_reset(message: types.Message):
    await db.set_bind(config.POSTGRES_URI)
    try:
        await Duel.__table__.gino.drop()
    except UndefinedTableError:
        pass
    try:
        await Effect.__table__.gino.drop()
    except UndefinedTableError:
        pass
    try:
        await InventoryWeapon.__table__.gino.drop()
    except UndefinedTableError:
        pass
    try:
        await InventoryOutfit.__table__.gino.drop()
    except UndefinedTableError:
        pass
    try:
        await InventoryMeal.__table__.gino.drop()
    except UndefinedTableError:
        pass
    try:
        await User.__table__.gino.drop()
    except UndefinedTableError:
        pass
    await all_init.all_init()
    await User.__table__.gino.create()
    await InventoryOutfit.__table__.gino.create()
    await InventoryWeapon.__table__.gino.create()
    await InventoryMeal.__table__.gino.create()
    await Effect.__table__.gino.create()
    await Duel.__table__.gino.create()
    await dp.bot.send_message(message.from_user.id, "База данных пересоздана")
