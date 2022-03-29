from asyncpg import UniqueViolationError

from utils.db_api.schemas.inventory_weapon import InventoryWeapon


async def add_inventory_weapon(user_id: int,
                               weapon_id: int):
    try:
        inventory_weapon = InventoryWeapon(
            user_id=user_id,
            amount=1,
            weapon_id=weapon_id
        )
        await inventory_weapon.create()

    except UniqueViolationError:
        inventory_weapon = await InventoryWeapon.query.where(
            InventoryWeapon.user_id == user_id and
            InventoryWeapon.weapon_id == weapon_id
        ).gino.first()
        await inventory_weapon.update(amount=inventory_weapon.amount + 1).apply()


async def discard_inventory_weapon(user_id: int,
                                   weapon_id: int):
    inventory_weapon = await InventoryWeapon.query.where(
        InventoryWeapon.user_id == user_id and
        InventoryWeapon.weapon_id == weapon_id
    ).gino.first()
    # await (db.select([db.func.count()])
    #        .where(and_(Meeting.status == MeetingStatus.SCHEDULED,
    #                    Meeting.start_at < some_time_from_now(window))))
    # .gino
    # .scalar())
    # )
    if inventory_weapon is None:
        print("Запись не найдена")
    else:
        print("Запись найдена")
