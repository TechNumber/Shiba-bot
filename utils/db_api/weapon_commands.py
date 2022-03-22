from asyncpg import UniqueViolationError

from utils.db_api.schemas.weapon import Weapon


async def add_weapon(weapon_id: int,
                     weapon_name: str,
                     weapon_price: int,
                     weapon_description: str,
                     weapon_chars: str,
                     damage: int,
                     agility_add: int,
                     agility_mpy: float,
                     health_add: int,
                     health_mpy: float
                     ):
    try:
        weapon = Weapon(
            weapon_id=weapon_id,
            weapon_name=weapon_name,
            weapon_price=weapon_price,
            weapon_description=weapon_description,
            weapon_chars=weapon_chars,
            damage=damage,
            agility_add=agility_add,
            agility_mpy=agility_mpy,
            health_add=health_add,
            health_mpy=health_mpy
        )
        await weapon.create()

    except UniqueViolationError:
        pass


async def select_all_weapons():
    weapons = await Weapon.query.gino.all()
    return weapons


async def select_weapon(weapon_id: int):
    weapon = await Weapon.query.where(Weapon.weapon_id == weapon_id).gino.first()
    return weapon
