from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.schemas.mob import Mob


async def add_mob(mob_id: int,
                  mob_name: str,
                  mob_description: str,
                  mob_chars: str,
                  mob_pic_url: str,
                  mob_health: int,
                  mob_strength: int,
                  mob_agility: int,
                  mob_level: int):
    try:
        mob = Mob(
            mob_id=mob_id,
            mob_name=mob_name,
            mob_description=mob_description,
            mob_chars=mob_chars,
            mob_pic_url=mob_pic_url,
            mob_health=mob_health,
            mob_strength=mob_strength,
            mob_agility=mob_agility,
            mob_level=mob_level
        )
        await mob.create()

    except UniqueViolationError:
        pass


async def select_all_mobs():
    mobs = await Mob.query.gino.all()
    return mobs


async def select_mob(mob_id: int):
    mob = await Mob.query.where(Mob.mob_id == mob_id).gino.first()
    return mob


async def generate_all_mobs_chars():
    mobs = await select_all_mobs()
    for mob in mobs:
        await mob.update(
            mob_chars=''.join([
                'Имя: {}\n'.format(mob.mob_name),
                'Описание: {}\n'.format(mob.mob_description),
                'Здоровье: {}\n'.format(mob.mob_health),
                'Сила: {}\n'.format(mob.mob_strength),
                'Ловкость: {}\n'.format(mob.mob_agility),
            ])
        ).apply()
