# ----------------------------------------------------------------------------
# Для создания исключительно этой таблицы при запуске конкретно из этого файла
# import asyncio
# from data import config
# from utils.db_api.db_gino import db
# ----------------------------------------------------------------------------
from asyncpg import UndefinedTableError

from utils.db_api import weapon_commands
from utils.db_api.schemas.weapon import Weapon


async def weapon_init():
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
        await Weapon.__table__.gino.drop()
    except UndefinedTableError:
        pass
    await Weapon.__table__.gino.create()

    await weapon_commands.add_weapon(
        weapon_id=1,
        weapon_name="Палка",
        weapon_price=10,
        weapon_description="Обычная деревянная палка. Достаточно прочная и увесистая, чтобы использовать в качестве оружия.",
        weapon_chars="Описание через format строки с выгрузкой эффектов",
        damage=30,
        agility_add=20,
        agility_mpy=1,
        health_add=0,
        health_mpy=1
    )
    await weapon_commands.add_weapon(
        weapon_id=2,
        weapon_name="Ржавый меч",
        weapon_price=70,
        weapon_description="Старинный прямой меч, покрытый ржавчиной. Тем не менее, этот клинок все еще достаточно острый.",
        weapon_chars="Описание через format строки с выгрузкой эффектов",
        damage=50,
        agility_add=10,
        agility_mpy=1,
        health_add=0,
        health_mpy=1
    )
    await weapon_commands.add_weapon(
        weapon_id=3,
        weapon_name="Дубина переговоров",
        weapon_price=150,
        weapon_description="Тяжелая стальная дубина. Подходит для нанесения тяжелых, но не слишком стремительных ударов.",
        weapon_chars="Описание через format строки с выгрузкой эффектов",
        damage=100,
        agility_add=-5,
        agility_mpy=1,
        health_add=0,
        health_mpy=1
    )
    await weapon_commands.add_weapon(
        weapon_id=4,
        weapon_name="Костяной зуб",
        weapon_price=200,
        weapon_description="Древняя катана, изготовленная из прочной кости. Легенда гласит, что этот меч изготовлен из зуба могущественного дракона.",
        weapon_chars="Описание через format строки с выгрузкой эффектов",
        damage=1000,
        agility_add=30,
        agility_mpy=1,
        health_add=0,
        health_mpy=1
    )
    await weapon_commands.add_weapon(
        weapon_id=5,
        weapon_name="Вампир",
        weapon_price=500,
        weapon_description="Загадочный клинок багряного цвета. Чары, заключенные в нем, увеличивают жизненную силу владельца.",
        weapon_chars="Описание через format строки с выгрузкой эффектов",
        damage=950,
        agility_add=30,
        agility_mpy=1,
        health_add=100,
        health_mpy=1
    )
    await weapon_commands.generate_all_weapons_chars()

# ----------------------------------------------------------------------------
# Для создания исключительно этой таблицы при запуске конкретно из этого файла
# loop = asyncio.get_event_loop()
# loop.run_until_complete(outfit_init())
# ----------------------------------------------------------------------------
