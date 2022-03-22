from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from loader import db
from utils.db_api import db_gino
from utils.db_api import all_init
from utils.db_api.schemas.user import User


async def on_startup(dispatcher):
    print("Подключаем БД")
    await db_gino.on_startup(dp)
    print("Готово")

    print("Чистим базу")
    # await db.gino.drop_all()
    await User.__table__.gino.drop()
    print("Готово")

    print("Создаём таблицы")
    # await db.gino.create_all()
    await User.__table__.gino.create()
    print("Готово")

    print("Инициализируем таблицы предметов")
    await all_init.all_init()
    print("Готово")

    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
