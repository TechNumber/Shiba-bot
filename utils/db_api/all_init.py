from utils.db_api.initialization import meal_init, outfit_init, weapon_init


async def all_init():
    await outfit_init.outfit_init()
    await meal_init.meal_init()
    await weapon_init.weapon_init()
