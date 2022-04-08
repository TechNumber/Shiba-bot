from asyncpg import UniqueViolationError

from utils.db_api.schemas.inventory_outfit import InventoryOutfit


async def add_inventory_outfit(user_id: int,
                               outfit_id: int):
    try:
        inventory_outfit = InventoryOutfit(
            entry_id=hash(str(user_id) + str(outfit_id)),
            user_id=user_id,
            amount=1,
            outfit_id=outfit_id
        )
        await inventory_outfit.create()

    except UniqueViolationError:
        inventory_outfit = await InventoryOutfit.query.where(
            InventoryOutfit.user_id == user_id and
            InventoryOutfit.outfit_id == outfit_id
        ).gino.first()
        await inventory_outfit.update(amount=inventory_outfit.amount + 1).apply()


async def discard_inventory_outfit(user_id: int,
                                   outfit_id: int):
    inventory_outfit = await InventoryOutfit.query.where(
        InventoryOutfit.user_id == user_id and
        InventoryOutfit.weapon_id == outfit_id
    ).gino.first()
    if inventory_outfit is not None:
        if inventory_outfit.amount > 1:
            await inventory_outfit.update(amount=inventory_outfit.amount - 1).apply()
        else:
            await inventory_outfit.delete()
    else:
        print("Запись не найдена")
