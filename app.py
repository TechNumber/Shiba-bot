from aiogram import executor
from asyncpg import UndefinedTableError

from loader import dp
import middlewares, filters, handlers
from utils.db_api.schemas.inventory_outfit import InventoryOutfit
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from loader import db
from utils.db_api import db_gino
from utils.db_api import all_init
from utils.db_api.schemas.user import User
from utils.db_api.schemas.duel import Duel
from utils.db_api.schemas.inventory_weapon import InventoryWeapon


async def on_startup(dispatcher):
    print("Подключаем БД")
    await db_gino.on_startup(dp)
    print("Готово")

    print("Чистим базу")
    # await db.gino.drop_all()
    try:
        await Duel.__table__.gino.drop()
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
        await User.__table__.gino.drop()
    except UndefinedTableError:
        pass
    print("Готово")

    print("Инициализируем таблицы предметов")
    await all_init.all_init()
    print("Готово")

    print("Создаём таблицы")
    # await db.gino.create_all()
    await User.__table__.gino.create()
    await InventoryOutfit.__table__.gino.create()
    await InventoryWeapon.__table__.gino.create()
    await Duel.__table__.gino.create()
    print("Готово")

    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
