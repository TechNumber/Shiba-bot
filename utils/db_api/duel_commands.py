import hashlib

from asyncpg import UniqueViolationError
from sqlalchemy import and_

from utils.db_api.db_gino import db
from utils.db_api.schemas.duel import Duel


async def add_duel(sender_id: int,
                   receiver_id: int):
    try:
        duel = Duel(
            duel_id=int(hashlib.sha256((str(sender_id) + str(receiver_id)).encode('utf-8')).hexdigest(), 16) % 10 ** 8,
            sender_id=sender_id,
            receiver_id=receiver_id,
        )
        await duel.create()

    except UniqueViolationError:
        pass


async def delete_duel(sender_id: int,
                      receiver_id: int):
    duel = await Duel.query.where(
        and_(
            Duel.sender_id == Duel.sender_id,
            Duel.receiver_id == Duel.receiver_id
        )
    ).gino.first()
    if duel is not None:
        duel.delete()
    else:
        print("Запись не найдена")


async def select_all_senders_id(receiver_id: int):
    duels = await Duel.query.where(
        Duel.receiver_id == receiver_id
    ).gino.load(Duel.sender_id).all()
    return duels
