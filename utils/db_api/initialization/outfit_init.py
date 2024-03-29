# ----------------------------------------------------------------------------
# Для создания исключительно этой таблицы при запуске конкретно из этого файла
# import asyncio
# from data import config
# from utils.db_api.db_gino import db
# ----------------------------------------------------------------------------
from asyncpg import UndefinedTableError

from utils.db_api import outfit_commands
from utils.db_api.schemas.outfit import Outfit


async def outfit_init():
    """
    Данная функция инициализирует записи в таблице предметов одежды.

    Returns:
        None
    """
    # ----------------------------------------------------------------------------
    # Для создания исключительно этой таблицы при запуске конкретно из этого файла
    # (для этого также необходимо раскомментировать две нижние строчки файла)
    # await db.set_bind(config.POSTGRES_URI)
    # ----------------------------------------------------------------------------

    try:
        await Outfit.__table__.gino.drop()
    except UndefinedTableError:
        pass
    await Outfit.__table__.gino.create()

    await outfit_commands.add_outfit(
        outfit_id=1,
        outfit_name="Ошейник",
        outfit_price=20,
        outfit_description="Ошейник из неплохой кожи. Не очень хорошо защищает, однако совсем не стесняет движения",
        outfit_chars="Описание через format строки с выгрузкой эффектов",
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
        outfit_price=70,
        outfit_description="Пальто из прочных материалов. Относительно неплохо защищает, но мешает свободно двигаться.",
        outfit_chars="Описание через format строки с выгрузкой эффектов",
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
        outfit_price=150,
        outfit_description="Тапочки, сделанные из шерсти некого диковинного зверя. В них заключено благословение, дарующее на удивление хорошую защиту.",
        outfit_chars="Описание через format строки с выгрузкой эффектов",
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
        outfit_price=200,
        outfit_description="Скромный доспех, сделанный из дерева. Неплохо защищает, но стесняет движения.",
        outfit_chars="Описание через format строки с выгрузкой эффектов",
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
        outfit_price=500,
        outfit_description="Набор брони, созданной из легкого, но очень прочного сплава. Дарует поразительную защиту без ущерба ловкости.",
        outfit_chars="Описание через format строки с выгрузкой эффектов",
        health_add=1000,
        health_mpy=1,
        agility_add=10,
        agility_mpy=1,
        strength_add=100,
        strength_mpy=1
    )
    await outfit_commands.generate_all_outfits_chars()

# ----------------------------------------------------------------------------
# Для создания исключительно этой таблицы при запуске конкретно из этого файла
# loop = asyncio.get_event_loop()
# loop.run_until_complete(outfit_init())
# ----------------------------------------------------------------------------
