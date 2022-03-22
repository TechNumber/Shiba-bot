from asyncpg import UniqueViolationError

from utils.db_api.schemas.meal import Meal


async def add_meal(meal_id: int,
                   meal_name: str,
                   meal_price: int,
                   meal_description: str,
                   meal_chars: str,
                   max_health_time: int,
                   max_health_add: int,
                   max_health_mpy: float,
                   health_time: int,
                   health_add: int,
                   health_mpy: float,
                   strength_time: int,
                   strength_add: int,
                   strength_mpy: float):
    try:
        meal = Meal(
            meal_id=meal_id,
            meal_name=meal_name,
            meal_price=meal_price,
            meal_description=meal_description,
            meal_chars=meal_chars,
            max_health_time=max_health_time,
            max_health_add=max_health_add,
            max_health_mpy=max_health_mpy,
            health_time=health_time,
            health_add=health_add,
            health_mpy=health_mpy,
            strength_time=strength_time,
            strength_add=strength_add,
            strength_mpy=strength_mpy
        )
        await meal.create()

    except UniqueViolationError:
        pass


async def select_all_meals():
    meals = await Meal.query.gino.all()
    return meals


async def select_meal(meal_id: int):
    meal = await Meal.query.where(Meal.meal_id == meal_id).gino.first()
    return meal
