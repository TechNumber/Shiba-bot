# ----------------------------------------------------------------------------
# Для создания исключительно этой таблицы при запуске конкретно из этого файла
# import asyncio
# from data import config
# from utils.db_api.db_gino import db
# ----------------------------------------------------------------------------
from asyncpg import UndefinedTableError

from utils.db_api import mob_commands
from utils.db_api.schemas.mob import Mob


async def mob_init():
    """
    Данная функция инициализирует записи в таблице предметов оружия.

    Returns:
        None
    """
    # ----------------------------------------------------------------------------
    # Для создания исключительно этой таблицы при запуске конкретно из этого файла
    # (для этого также необходимо раскомментировать две нижние строчки файла)
    # await db.set_bind(config.POSTGRES_URI)
    # ----------------------------------------------------------------------------

    try:
        await Mob.__table__.gino.drop()
    except UndefinedTableError:
        pass
    await Mob.__table__.gino.create()

    await mob_commands.add_mob(
        mob_id=1,
        mob_name="Боб",
        mob_description="Просто Боб",
        mob_chars="",
        mob_pic_url="",
        mob_health=10,
        mob_strength=1,
        mob_agility=1,
        mob_level=1
    )
    await mob_commands.generate_all_mobs_chars()

# ----------------------------------------------------------------------------
# Для создания исключительно этой таблицы при запуске конкретно из этого файла
# loop = asyncio.get_event_loop()
# loop.run_until_complete(outfit_init())
# ----------------------------------------------------------------------------
