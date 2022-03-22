from utils.db_api.initialization import food_init, clothes_init, weapons_init


async def all_init():
    await clothes_init.clothes_init()
    await food_init.food_init()
    await weapons_init.weapons_init()
