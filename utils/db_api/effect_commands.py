import hashlib

from asyncpg import UniqueViolationError
from sqlalchemy import and_

from utils.db_api.meal_commands import select_meal
from utils.db_api.outfit_commands import select_outfit
from utils.db_api.schemas.effect import Effect
from utils.db_api.schemas.meal import Meal
from utils.db_api.schemas.user import User
from utils.db_api.weapon_commands import select_weapon


async def heal(user: User, healing: int):
    meal_id_list = await select_user_current_meals(user.user_id)
    max_hp_buffs = [0, 1] # прибавка и множитель
    for meal_id in meal_id_list:
        cur_meal = await select_meal(meal_id)
        max_hp_buffs[0] += cur_meal.max_health_add
        max_hp_buffs[1] *= cur_meal.max_health_mpy
    weapon = await select_weapon(user.weapon_id)
    if weapon is not None:
        max_hp_buffs[0] += weapon.health_add
        max_hp_buffs[1] *= weapon.health_mpy
    outfit = await select_outfit(user.outfit_id)
    if outfit is not None:
        max_hp_buffs[0] += outfit.health_add
        max_hp_buffs[1] *= outfit.health_mpy
    max_hp = user.max_health * max_hp_buffs[1] + max_hp_buffs[0]
    cur_hp = user.health
    cur_hp += healing
    if cur_hp > max_hp:
        cur_hp = max_hp
    await user.update(health=cur_hp).apply()


async def add_effect(user: User,
                     meal: Meal):
    # max_health_time = await Meal.select('max_health_time').where(Meal.meal_id == meal_id).gino.scalar()
    # health_time = await Meal.select('health_time').where(Meal.meal_id == meal_id).gino.scalar()
    # strength_time = await Meal.select('strength_time').where(Meal.meal_id == meal_id).gino.scalar()
    # agility_time = await Meal.select('agility_time').where(Meal.meal_id == meal_id).gino.scalar()
    effect_id = int(hashlib.sha256((str(user.user_id) + str(meal.meal_id)).encode('utf-8')).hexdigest(), 16) % 10 ** 8
    try:
        effect = Effect(
            effect_id=effect_id,
            user_id=user.user_id,
            meal_id=meal.meal_id,
            max_health_duration=meal.max_health_time,
            strength_duration=meal.strength_time,
            agility_duration=meal.agility_time,
        )
        await effect.create()
    except UniqueViolationError:
        effect = await Effect.query.where(
            and_(
                Effect.user_id == user.user_id,
                Effect.effect_id == effect_id
            )
        ).gino.first()
        await effect.update(
            max_health_duration=effect.max_health_duration + meal.max_health_time,
            strength_duration=effect.strength_duration + meal.strength_time,
            agility_duration=effect.agility_duration + meal.agility_time
        ).apply()
    await heal(user, meal.health_add)


async def delete_effect(user_id: int, meal_id):
    effect = await Effect.query.where(
        (
            Effect.user_id == user_id,
            Effect.meal_id == meal_id
        )
    ).gino.first()
    if effect is not None:
        effect.delete()
    else:
        print("Запись не найдена")


async def reduce_duration(user_id: int):
    await Effect.update.values(
        max_health_duration=Effect.max_health_duration - 1
    ).where(
        and_(
            Effect.max_health_duration > 0,
            Effect.user_id == user_id
        )
    ).gino.status()
    await Effect.update.values(
        strength_duration=Effect.strength_duration - 1
    ).where(
        and_(
            Effect.strength_duration > 0,
            Effect.user_id == user_id
        )
    ).gino.status()
    await Effect.update.values(
        agility_duration=Effect.agility_duration - 1
    ).where(
        and_(
            Effect.agility_duration > 0,
            Effect.user_id == user_id
        )
    ).gino.status()
    await Effect.delete.where(
        and_(
            Effect.max_health_duration == 0,
            Effect.strength_duration == 0,
            Effect.agility_duration == 0
        )
    ).gino.status()


async def select_user_current_meals(user_id: int):
    meals = await Effect.query.where(
        Effect.user_id == user_id
    ).gino.load(Effect.meal_id).all()
    return meals
