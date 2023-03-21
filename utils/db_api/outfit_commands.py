from decimal import Decimal

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


async def generate_all_outfits_chars():
    outfit = await select_all_outfits()
    for outfit in outfit:
        await outfit.update(
            outfit_chars=''.join([
                'Название: {}\n'.format(outfit.outfit_name),
                'Цена: {}\n'.format(outfit.outfit_price),
                'Описание: {}\n'.format(outfit.outfit_description),
                'На сколько единиц увеличивает здоровье: {}\n'.format(
                    outfit.health_add
                ) if outfit.health_add != 0 else '',
                'Во сколько раз увеличивает здоровье: {}\n'.format(
                    Decimal(outfit.health_mpy).quantize(Decimal('.1')).normalize()
                ) if outfit.health_mpy != 1 else '',

                'На сколько единиц увеличивает ловкость: {}\n'.format(
                    outfit.agility_add
                ) if outfit.agility_add != 0 else '',
                'Во сколько раз увеличивает ловкость: {}\n'.format(
                    Decimal(outfit.agility_mpy).quantize(Decimal('.1')).normalize()
                ) if outfit.agility_mpy != 1 else '',

                'На сколько единиц увеличивает силу: {}\n'.format(
                    outfit.strength_add
                ) if outfit.strength_add != 0 else '',
                'Во сколько раз увеличивает силу: {}\n'.format(
                    Decimal(outfit.strength_mpy).quantize(Decimal('.1')).normalize()
                ) if outfit.strength_mpy != 1 else ''
            ])
        ).apply()
