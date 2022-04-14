from utils.db_api.initialization import meal_init, outfit_init, weapon_init


async def all_init():
    """
    Данная фукнция запускает функции инициализации таблиц еды, оружия и одежды,
    присутствующих в игре.

    Returns:
        None
    """
    await outfit_init.outfit_init()
    await meal_init.meal_init()
    await weapon_init.weapon_init()
