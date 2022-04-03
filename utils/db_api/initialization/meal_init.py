# ----------------------------------------------------------------------------
# Для создания исключительно этой таблицы при запуске конкретно из этого файла
# import asyncio
# from data import config
# from utils.db_api.db_gino import db
# ----------------------------------------------------------------------------
from asyncpg import UndefinedTableError

from utils.db_api import meal_commands
from utils.db_api.schemas.meal import Meal


async def meal_init():
    # ----------------------------------------------------------------------------
    # Для создания исключительно этой таблицы при запуске конкретно из этого файла
    # await db.set_bind(config.POSTGRES_URI)
    # await db.gino.drop_all()
    # await db.gino.create_all()
    # ----------------------------------------------------------------------------

    # ------------------------------------
    # Для версии без внешних ключей
    try:
        await Meal.__table__.gino.drop()
    except UndefinedTableError:
        pass
    await Meal.__table__.gino.create()
    # ------------------------------------
    await meal_commands.add_meal(
        meal_id=1,
        meal_name="Сухой корм",
        meal_price=25,
        meal_description="Описание",
        meal_chars="Описание через f строки с выгрузкой эффектов",
        max_health_time=0,
        max_health_add=0,
        max_health_mpy=1,
        health_time=0,
        health_add=20,
        health_mpy=1,
        strength_time=0,
        strength_add=0,
        strength_mpy=1
    )
    await meal_commands.add_meal(
        meal_id=2,
        meal_name="Говяжья кость",
        meal_price=70,
        meal_description="Описание",
        meal_chars="Описание через f строки с выгрузкой эффектов",
        max_health_time=0,
        max_health_add=0,
        max_health_mpy=1,
        health_time=0,
        health_add=30,
        health_mpy=1,
        strength_time=5,
        strength_add=0,
        strength_mpy=1.2
    )
    await meal_commands.add_meal(
        meal_id=3,
        meal_name="Листик мяты",
        meal_price=250,
        meal_description="Описание",
        meal_chars="Описание через f строки с выгрузкой эффектов",
        max_health_time=0,
        max_health_add=0,
        max_health_mpy=1,
        health_time=0,
        health_add=100,
        health_mpy=1,
        strength_time=0,
        strength_add=0,
        strength_mpy=1.5
    )
    await meal_commands.add_meal(
        meal_id=4,
        meal_name="Утиная грудка",
        meal_price=200,
        meal_description="Описание",
        meal_chars="Описание через f строки с выгрузкой эффектов",
        max_health_time=0,
        max_health_add=0,
        max_health_mpy=1,
        health_time=0,
        health_add=100,
        health_mpy=1,
        strength_time=0,
        strength_add=0,
        strength_mpy=1
    )
    await meal_commands.add_meal(
        meal_id=5,
        meal_name="Каре ягненка",
        meal_price=200,
        meal_description="Описание",
        meal_chars="Описание через f строки с выгрузкой эффектов",
        max_health_time=0,
        max_health_add=0,
        max_health_mpy=1,
        health_time=0,
        health_add=0,
        health_mpy=1,
        strength_time=5,
        strength_add=0,
        strength_mpy=2
    )
    await meal_commands.add_meal(
        meal_id=6,
        meal_name="Черная икра",
        meal_price=1000,
        meal_description="Описание",
        meal_chars="Описание через f строки с выгрузкой эффектов",
        max_health_time=0,
        max_health_add=0,
        max_health_mpy=1,
        health_time=0,
        health_add=0,
        health_mpy=-1,  # коэффициент умножения -1 == полное восстановление здоровья
        strength_time=0,
        strength_add=0,
        strength_mpy=3
    )
    await meal_commands.add_meal(
        meal_id=7,
        meal_name="Фуа-гра",
        meal_price=10000,
        meal_description="Описание",
        meal_chars="Описание через f строки с выгрузкой эффектов",
        max_health_time=0,
        max_health_add=1000,
        max_health_mpy=1,
        health_time=0,
        health_add=1000,
        health_mpy=1,
        strength_time=0,
        strength_add=0,
        strength_mpy=1
    )

# ----------------------------------------------------------------------------
# Для создания исключительно этой таблицы при запуске конкретно из этого файла
# loop = asyncio.get_event_loop()
# loop.run_until_complete(meal_init())
# ----------------------------------------------------------------------------
