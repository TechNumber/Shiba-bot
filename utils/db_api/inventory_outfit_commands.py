import hashlib

from asyncpg import UniqueViolationError
from sqlalchemy import and_

from utils.db_api.schemas.inventory_outfit import InventoryOutfit


async def add_inventory_outfit(user_id: int,
                               outfit_id: int):
    try:
        inventory_outfit = InventoryOutfit(
            entry_id=int(hashlib.sha256((str(user_id) + str(outfit_id)).encode('utf-8')).hexdigest(), 16) % 10 ** 8,
            user_id=user_id,
            amount=1,
            outfit_id=outfit_id
        )
        await inventory_outfit.create()

    except UniqueViolationError:
        inventory_outfit = await InventoryOutfit.query.where(
            and_(
                InventoryOutfit.user_id == user_id,
                InventoryOutfit.outfit_id == outfit_id
            )
        ).gino.first()
        await inventory_outfit.update(amount=inventory_outfit.amount + 1).apply()


async def discard_inventory_outfit(user_id: int,
                                   outfit_id: int):
    inventory_outfit = await InventoryOutfit.query.where(
        and_(
            InventoryOutfit.user_id == user_id,
            InventoryOutfit.weapon_id == outfit_id
        )
    ).gino.first()
    if inventory_outfit is not None:
        if inventory_outfit.amount > 1:
            await inventory_outfit.update(amount=inventory_outfit.amount - 1).apply()
        else:
            await inventory_outfit.delete()
    else:
        print("Запись не найдена")
