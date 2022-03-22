# ----------------------------------------------------------------------------
# Для создания исключительно этой таблицы при запуске конкретно из этого файла
# import asyncio
# from data import config
# from utils.db_api.db_gino import db
# ----------------------------------------------------------------------------

from utils.db_api import outfit_commands
from utils.db_api.schemas.outfit import Outfit


async def outfit_init():
    # ----------------------------------------------------------------------------
    # Для создания исключительно этой таблицы при запуске конкретно из этого файла
    # await db.set_bind(config.POSTGRES_URI)
    # await db.gino.drop_all()
    # await db.gino.create_all()
    # ----------------------------------------------------------------------------

    # ------------------------------------
    # Для версии без внешних ключей
    # await Outfit.__table__.gino.drop()
    # await Outfit.__table__.gino.create()
    # ------------------------------------
    await outfit_commands.add_outfit(
        outfit_id=1,
        outfit_name="Ошейник",
        outfit_price=0,
        outfit_description="Описание",
        outfit_chars="Описание через f строки с выгрузкой эффектов",
        health_add=10,
        health_mpy=1,
        agility_add=40,
        agility_mpy=1,
        strength_add=0,
        strength_mpy=1
    )
    await outfit_commands.add_outfit(
        outfit_id=2,
        outfit_name="Пальто",
        outfit_price=0,
        outfit_description="Описание",
        outfit_chars="Описание через f строки с выгрузкой эффектов",
        health_add=50,
        health_mpy=1,
        agility_add=-10,
        agility_mpy=1,
        strength_add=0,
        strength_mpy=1
    )
    await outfit_commands.add_outfit(
        outfit_id=3,
        outfit_name="Белые тапочки",
        outfit_price=0,
        outfit_description="Описание",
        outfit_chars="Описание через f строки с выгрузкой эффектов",
        health_add=100,
        health_mpy=1,
        agility_add=10,
        agility_mpy=1,
        strength_add=0,
        strength_mpy=1
    )
    await outfit_commands.add_outfit(
        outfit_id=4,
        outfit_name="Деревянный нагрудник",
        outfit_price=0,
        outfit_description="Описание",
        outfit_chars="Описание через f строки с выгрузкой эффектов",
        health_add=100,
        health_mpy=1,
        agility_add=-10,
        agility_mpy=1,
        strength_add=0,
        strength_mpy=1
    )
    await outfit_commands.add_outfit(
        outfit_id=5,
        outfit_name="Металлические латы",
        outfit_price=0,
        outfit_description="Описание",
        outfit_chars="Описание через f строки с выгрузкой эффектов",
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
# loop.run_until_complete(outfit_init())
# ----------------------------------------------------------------------------
