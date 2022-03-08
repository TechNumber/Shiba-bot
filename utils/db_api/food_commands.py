from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.schemas.food import Food


async def add_food(food_id: int, food_name: str, food_price: int, food_description: str,
                   food_chars: str, max_health_time: int, max_health_add: int,
                   max_health_mpy: int, health_time: int, health_add: int,
                   health_mpy: float, strength_time: int, strength_add: int,
                   strength_mpy: float):
    try:
        food = Food(food_id=food_id, food_name=food_name, food_price=food_price,
                    food_description=food_description, food_chars=food_chars,
                    max_health_time=max_health_time, max_health_add=max_health_add,
                    max_health_mpy=max_health_mpy, health_time=health_time,
                    health_add=health_add, health_mpy=health_mpy,
                    strength_time=strength_time, strength_add=strength_add,
                    strength_mpy=strength_mpy)
        await food.create()

    except UniqueViolationError:
        pass


async def select_all_food():
    food = await Food.query.gino.all()
    return food


async def select_food(food_id: int):
    food = await Food.query.where(Food.food_id == food_id).gino.first()
    return food
