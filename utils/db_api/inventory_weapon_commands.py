import hashlib

from asyncpg import UniqueViolationError
from sqlalchemy import and_

from utils.db_api import weapon_commands, user_commands
from utils.db_api.schemas.inventory_weapon import InventoryWeapon


async def add_inventory_weapon(user_id: int,
                               weapon_id: int):
    try:
        inventory_weapon = InventoryWeapon(
            entry_id=int(hashlib.sha256((str(user_id) + str(weapon_id)).encode('utf-8')).hexdigest(), 16) % 10 ** 8,
            user_id=user_id,
            amount=1,
            weapon_id=weapon_id
        )
        await inventory_weapon.create()

    except UniqueViolationError:
        inventory_weapon = await InventoryWeapon.query.where(
            and_(
                InventoryWeapon.user_id == user_id,
                InventoryWeapon.weapon_id == weapon_id
            )
        ).gino.first()
        await inventory_weapon.update(amount=inventory_weapon.amount + 1).apply()


async def discard_inventory_weapon(user_id: int,
                                   weapon_id: int):
    inventory_weapon = await InventoryWeapon.query.where(
        and_(
            InventoryWeapon.user_id == user_id,
            InventoryWeapon.weapon_id == weapon_id
        )
    ).gino.first()
    if inventory_weapon is not None:
        if inventory_weapon.amount > 1:
            await inventory_weapon.update(amount=inventory_weapon.amount - 1).apply()
        else:
            await inventory_weapon.delete()
            await user_commands.set_weapon_null(user_id=user_id)
    else:
        print("Запись не найдена")


async def select_all_weapons_by_user_id(user_id: int):
    entries = await InventoryWeapon.query.where(
        InventoryWeapon.user_id == user_id
    ).gino.all()
    weapons = [await weapon_commands.select_weapon(entry.weapon_id) for entry in entries]
    return weapons


async def get_weapon_amount(user_id: int, weapon_id: int):
    entry = await InventoryWeapon.query.where(
        and_(
            InventoryWeapon.user_id == user_id,
            InventoryWeapon.weapon_id == weapon_id
        )
    ).gino.first()
    return entry.amount
