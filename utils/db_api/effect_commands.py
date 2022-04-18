import hashlib

from asyncpg import UniqueViolationError
from sqlalchemy import and_

from utils.db_api.schemas.effect import Effect
from utils.db_api.schemas.meal import Meal


async def add_effect(user_id: int,
                     meal_id: int):
    max_health_time = await Meal.select('max_health_time').where(Meal.meal_id == meal_id).gino.scalar()
    health_time = await Meal.select('health_time').where(Meal.meal_id == meal_id).gino.scalar()
    strength_time = await Meal.select('strength_time').where(Meal.meal_id == meal_id).gino.scalar()
    agility_time = await Meal.select('agility_time').where(Meal.meal_id == meal_id).gino.scalar()
    effect_id = int(hashlib.sha256((str(user_id) + str(meal_id)).encode('utf-8')).hexdigest(), 16) % 10 ** 8
    try:
        effect = Effect(
            effect_id=effect_id,
            user_id=user_id,
            meal_id=meal_id,
            max_health_duration=max_health_time,
            health_duration=health_time,
            strength_duration=strength_time,
            agility_duration=agility_time,
        )
        await effect.create()

    except UniqueViolationError:
        effect = await effect.query.where(
            and_(
                effect.user_id == user_id,
                effect.effect_id == effect_id
            )
        ).gino.first()
        await effect.update(max_health_duration=effect.max_health_duration + max_health_time).apply()
        await effect.update(health_duration=effect.max_health_duration + health_time).apply()
        await effect.update(strength_duration=effect.max_health_duration + strength_time).apply()
        await effect.update(agility_time=effect.max_health_duration + agility_time).apply()


async def delete_effect(effect_id: int):
    effect = await Effect.query.where(
        (
            Effect.effect_id == effect_id,
        )
    ).gino.first()
    if effect is not None:
        effect.delete()
    else:
        print("Запись не найдена")


async def reduce_duration(user_id: int):
    await Effect.update.values(
        max_health_duration=Effect.max_health_duration - 1).where(
            and_(
                Effect.max_health_duration > 0,
                Effect.user_id == user_id
            )
        ).gino.status()
    await Effect.update.values(
        health_duration=Effect.health_duration - 1).where(
        and_(
            Effect.health_duration > 0,
            Effect.user_id == user_id
        )
    ).gino.status()
    await Effect.update.values(
        strength_duration=Effect.strength_duration - 1).where(
        and_(
            Effect.strength_duration > 0,
            Effect.user_id == user_id
        )
    ).gino.status()
    await Effect.update.values(
        agility_duration=Effect.agility_duration - 1).where(
        and_(
            Effect.agility_duration > 0,
            Effect.user_id == user_id
        )
    ).gino.status()
    await Effect.delete.where(
        and_(
            Effect.max_health_duration == 0,
            Effect.health_duration == 0,
            Effect.strength_duration == 0,
            Effect.agility_duration == 0
        )
    )
