# ----------------------------------------------------------------------------
# Для создания исключительно этой таблицы при запуске конкретно из этого файла
# import asyncio
# from data import config
# from utils.db_api.db_gino import db
# ----------------------------------------------------------------------------

from utils.db_api import clothes_commands
from utils.db_api.schemas.clothes import Clothes


async def clothes_init():
    # ----------------------------------------------------------------------------
    # Для создания исключительно этой таблицы при запуске конкретно из этого файла
    # await db.set_bind(config.POSTGRES_URI)
    # await db.gino.drop_all()
    # await db.gino.create_all()
    # ----------------------------------------------------------------------------

    # ------------------------------------
    # Для версии без внешних ключей
    # await Clothes.__table__.gino.drop()
    # await Clothes.__table__.gino.create()
    # ------------------------------------
    await clothes_commands.add_clothes(
        clothes_id=1,
        clothes_name="Ошейник",
        clothes_price=0,
        clothes_description="Описание",
        clothes_chars="Описание через f строки с выгрузкой эффектов",
        health_add=10,
        health_mpy=1,
        agility_add=40,
        agility_mpy=1,
        strength_add=0,
        strength_mpy=1
    )
    await clothes_commands.add_clothes(
        clothes_id=2,
        clothes_name="Пальто",
        clothes_price=0,
        clothes_description="Описание",
        clothes_chars="Описание через f строки с выгрузкой эффектов",
        health_add=50,
        health_mpy=1,
        agility_add=-10,
        agility_mpy=1,
        strength_add=0,
        strength_mpy=1
    )
    await clothes_commands.add_clothes(
        clothes_id=3,
        clothes_name="Белые тапочки",
        clothes_price=0,
        clothes_description="Описание",
        clothes_chars="Описание через f строки с выгрузкой эффектов",
        health_add=100,
        health_mpy=1,
        agility_add=10,
        agility_mpy=1,
        strength_add=0,
        strength_mpy=1
    )
    await clothes_commands.add_clothes(
        clothes_id=4,
        clothes_name="Деревянный нагрудник",
        clothes_price=0,
        clothes_description="Описание",
        clothes_chars="Описание через f строки с выгрузкой эффектов",
        health_add=100,
        health_mpy=1,
        agility_add=-10,
        agility_mpy=1,
        strength_add=0,
        strength_mpy=1
    )
    await clothes_commands.add_clothes(
        clothes_id=5,
        clothes_name="Металлические латы",
        clothes_price=0,
        clothes_description="Описание",
        clothes_chars="Описание через f строки с выгрузкой эффектов",
        health_add=1000,
        health_mpy=1,
        agility_add=10,
        agility_mpy=1,
        strength_add=100,
        strength_mpy=1
    )

# ----------------------------------------------------------------------------
# Для создания исключительно этой таблицы при запуске конкретно из этого файла
# loop = asyncio.get_event_loop()
# loop.run_until_complete(clothes_init())
# ----------------------------------------------------------------------------
