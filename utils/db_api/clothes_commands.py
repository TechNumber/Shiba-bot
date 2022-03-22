from asyncpg import UniqueViolationError

from utils.db_api.schemas.clothes import Clothes


async def add_clothes(clothes_id: int,
                      clothes_name: str,
                      clothes_price: int,
                      clothes_description: str,
                      clothes_chars: str,
                      health_add: int,
                      health_mpy: float,
                      agility_add: int,
                      agility_mpy: float,
                      strength_add: int,
                      strength_mpy: float):
    try:
        clothes = Clothes(
            clothes_id=clothes_id,
            clothes_name=clothes_name,
            clothes_price=clothes_price,
            clothes_description=clothes_description,
            clothes_chars=clothes_chars,
            health_add=health_add,
            health_mpy=health_mpy,
            agility_add=agility_add,
            agility_mpy=agility_mpy,
            strength_add=strength_add,
            strength_mpy=strength_mpy
        )
        await clothes.create()

    except UniqueViolationError:
        pass


async def select_all_clothes():
    clothes = await Clothes.query.gino.all()
    return clothes


async def select_clothes(clothes_id: int):
    clothes = await Clothes.query.where(Clothes.food_id == clothes_id).gino.first()
    return clothes
