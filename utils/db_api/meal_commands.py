import asyncio
import math
from decimal import Decimal

from asyncpg import UniqueViolationError

from utils.db_api import user_commands
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
                   strength_mpy: float,
                   agility_time: int,
                   agility_add: int,
                   agility_mpy: float
                   ):
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
            strength_mpy=strength_mpy,
            agility_time=agility_time,
            agility_add=agility_add,
            agility_mpy=agility_mpy
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
                'На сколько ходов увеличивает максимальное здоровье: {}\n'.format(
                    meal.max_health_time
                ) if meal.max_health_time != 0 else '',
                'На сколько единиц увеличивает максимальное здоровье: {}\n'.format(
                    meal.max_health_add
                ) if meal.max_health_add != 0 else '',
                'Во сколько раз увеличивает максимальное здоровье: {}\n'.format(
                    Decimal(meal.max_health_mpy).quantize(Decimal('.1')).normalize()
                ) if meal.max_health_mpy != 1 else '',

                'На сколько ходов увеличивает здоровье: {}\n'.format(
                    meal.health_time
                ) if meal.health_time != 0 else '',
                'На сколько единиц увеличивает здоровье: {}\n'.format(
                    meal.health_add
                ) if meal.health_add != 0 else '',
                'Полностью восстанавливает здоровье\n' if meal.health_mpy == -1 else
                'Во сколько раз увеличивает здоровье: {}\n'.format(
                    Decimal(meal.health_mpy).quantize(Decimal('.1')).normalize()
                ) if meal.health_mpy != 1 else '',

                'На сколько ходов увеличивает силу: {}\n'.format(
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


# --------------------------------------------------------------------------------
# Ниже расположена старая версия функции apply_meal_effects, работающая с временем
# (asyncio.sleep). Все функции increase_effect и delay_effect закомментированы,
# поскольку они непосредственно изменяют показатели пользователя в БД, от чего
# мы отказываемся в реализации со счётчиком дуэлей и обособленными коэффициентами
# умножения и добавления.
# --------------------------------------------------------------------------------
"""
async def increase_max_health(user_id: int, meal):
    user = await user_commands.select_user(user_id=user_id)
    await user.update(max_health=math.ceil(user.max_health * meal.max_health_mpy + meal.max_health_add)).apply()
    print(f"Получил пользователя: {user}")


async def delay_max_health(user_id, meal):
    user = await user_commands.select_user(user_id=user_id)
    await asyncio.sleep(meal.max_health_time * 60)
    await user.update(max_health=math.ceil(user.max_health / meal.max_health_mpy - meal.max_health_add)).apply()
    print(f"Получил пользователя: {user}")


async def increase_health(user_id: int, meal):
    user = await user_commands.select_user(user_id=user_id)
    # TODO: здоровье после увеличения не может превышать максимальное.
    #  Но это затруднит возвращение здоровья к исходному значению после окончания действия эффекта.
    #  Поэтому лучше обрабатывать этот случай где-то в функции, которая отвечает за расчёт здоровья
    #  в бою, а не в БД. If'ом каким-нибудь.
    await user.update(health=math.ceil(user.health * meal.health_mpy + meal.health_add)).apply()
    print(f"Получил пользователя: {user}")


async def delay_health(user_id, meal):
    user = await user_commands.select_user(user_id=user_id)
    await asyncio.sleep(meal.health_time * 60)
    await user.update(health=math.ceil(user.health / meal.health_mpy - meal.health_add)).apply()
    print(f"Получил пользователя: {user}")


async def increase_strength(user_id: int, meal):
    user = await user_commands.select_user(user_id=user_id)
    await user.update(strength=math.ceil(user.strength * meal.strength_mpy + meal.strength_add)).apply()
    print(f"Получил пользователя: {user}")


async def delay_strength(user_id, meal):
    user = await user_commands.select_user(user_id=user_id)
    await asyncio.sleep(meal.strength_time * 60)
    await user.update(strength=math.ceil(user.strength / meal.strength_mpy - meal.strength_add)).apply()
    print(f"Получил пользователя: {user}")
"""

"""
async def apply_meal_effects(user_id: int, meal_id: int):
    user = await user_commands.select_user(user_id=user_id)
    meal = await select_meal(meal_id=meal_id)
    if meal.max_health_time != 0:
        tasks = [
            increase_max_health(user_id, meal),
            delay_max_health(user_id, meal)
        ]
        await asyncio.gather(*tasks)
    else:
        await user.update(max_health=math.ceil(user.max_health * meal.max_health_mpy + meal.max_health_add)).apply()
    if meal.health_mpy == -1:
        await user.update(health=user.max_health).apply()
    elif meal.health_time != 0:
        tasks = [
            increase_health(user_id, meal),
            delay_health(user_id, meal)
        ]
        await asyncio.gather(*tasks)
    else:
        await user.update(health=math.ceil(user.health * meal.health_mpy + meal.health_add)).apply()

    if meal.strength_time != 0:
        tasks = [
            increase_strength(user_id, meal),
            delay_strength(user_id, meal)
        ]
        await asyncio.gather(*tasks)
    else:
        await user.update(strength=math.ceil(user.strength * meal.strength_mpy + meal.strength_add)).apply()
"""
# TODO: показатель не может упасть ниже нуля
