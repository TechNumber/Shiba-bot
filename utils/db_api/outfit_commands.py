from asyncpg import UniqueViolationError

from utils.db_api.schemas.outfit import Outfit


async def add_outfit(outfit_id: int,
                      outfit_name: str,
                      outfit_price: int,
                      outfit_description: str,
                      outfit_chars: str,
                      health_add: int,
                      health_mpy: float,
                      agility_add: int,
                      agility_mpy: float,
                      strength_add: int,
                      strength_mpy: float):
    try:
        outfit = Outfit(
            outfit_id=outfit_id,
            outfit_name=outfit_name,
            outfit_price=outfit_price,
            outfit_description=outfit_description,
            outfit_chars=outfit_chars,
            health_add=health_add,
            health_mpy=health_mpy,
            agility_add=agility_add,
            agility_mpy=agility_mpy,
            strength_add=strength_add,
            strength_mpy=strength_mpy
        )
        await outfit.create()

    except UniqueViolationError:
        pass


async def select_all_outfits():
    outfits = await Outfit.query.gino.all()
    return outfits


async def select_outfit(outfit_id: int):
    outfit = await Outfit.query.where(Outfit.outfit_id == outfit_id).gino.first()
    return outfit
