import hashlib

from asyncpg import UniqueViolationError
from sqlalchemy import and_

from utils.db_api.db_gino import db
from utils.db_api.schemas.duel import Duel


async def add_duel(sender_id: int,
                   receiver_id: int):
    """
    Функция добавляет новую запись о запросе на дуэль в таблицу дуэлей.

    Args:
        sender_id (int): ID пользователя, отправившего запрос на дуэль.
        receiver_id (int):  ID пользователя, кому был отправлен запрос на дуэль.

    Returns:
        None
    """
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
    """
    Функция удаляет запись о запросе на дуэль из таблицы дуэлей.

    Args:
        sender_id (int): ID пользователя, отправившего запрос на дуэль.
        receiver_id (int): ID пользователя, кому был отправлен запрос на дуэль.

    Returns:
        None
    """
    duel = await Duel.query.where(
        and_(
            Duel.sender_id == sender_id,
            Duel.receiver_id == receiver_id
        )
    ).gino.first()
    if duel is not None:
        await duel.delete()
    else:
        print("Запись не найдена")


async def select_all_senders_id(receiver_id: int):
    """
    Функция возвращает ID всех пользователей, которые отправили запрос на дуэль
    определённому пользователю.

    Args:
        receiver_id: ID пользователя, кому был отправлен запрос на дуэль.

    Returns:
        (list): Список ID всех пользователей, которые отправили запрос на дуэль
        пользователю с ID receiver_id.
    """
    duels = await Duel.query.where(
        Duel.receiver_id == receiver_id
    ).gino.load(Duel.sender_id).all()
    return duels
