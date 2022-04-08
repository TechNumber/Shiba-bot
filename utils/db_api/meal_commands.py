from decimal import Decimal

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


async def generate_all_meals_chars():
    meals = await select_all_meals()
    for meal in meals:
        await meal.update(
            meal_chars=''.join([
                'Название: {}\n'.format(meal.meal_name),
                'Цена: {}\n'.format(meal.meal_price),
                'Описание: {}\n'.format(meal.meal_description),
                'На сколько минут увеличивает максимальное здоровье: {}\n'.format(
                    meal.max_health_time
                ) if meal.max_health_time != 0 else '',
                'На сколько единиц увеличивает максимальное здоровье: {}\n'.format(
                    meal.max_health_add
                ) if meal.max_health_add != 0 else '',
                'Во сколько раз увеличивает максимальное здоровье: {}\n'.format(
                    Decimal(meal.max_health_mpy).quantize(Decimal('.1')).normalize()
                ) if meal.max_health_mpy != 1 else '',

                'На сколько минут увеличивает здоровье: {}\n'.format(
                    meal.health_time
                ) if meal.health_time != 0 else '',
                'На сколько единиц увеличивает здоровье: {}\n'.format(
                    meal.health_add
                ) if meal.health_add != 0 else '',
                'Полностью восстанавливает здоровье\n' if meal.health_mpy == -1 else
                'Во сколько раз увеличивает здоровье: {}\n'.format(
                    Decimal(meal.health_mpy).quantize(Decimal('.1')).normalize()
                ) if meal.health_mpy != 1 else '',

                'На сколько минут увеличивает силу: {}\n'.format(
                    meal.strength_time
                ) if meal.strength_time != 0 else '',
                'На сколько единиц увеличивает силу: {}\n'.format(
                    meal.strength_add
                ) if meal.strength_add != 0 else '',
                'Во сколько раз увеличивает силу: {}\n'.format(
                    Decimal(meal.strength_mpy).quantize(Decimal('.1')).normalize()
                ) if meal.strength_mpy != 1 else ''
            ])
        ).apply()
