from sqlalchemy import Column, Integer, sql, BigInteger, ForeignKey

from utils.db_api.db_gino import TimedBaseModel


class Duel(TimedBaseModel):
    """
    Таблица всех запросов на дуэль.

    Columns:
        duel_id (int, PK): ID записи о дуэли
        sender_id (int, FK): ID пользователя, отправившего запрос на дуэль. Поле
        связано внешним ключом с полем user_id таблицы User.
        receiver_id (int, FK): ID пользователя, которому отправлен запрос на дуэль.
        Поле связано внешним ключом с полем user_id таблицы User.
    """
    __tablename__ = 'duels'
    duel_id = Column(BigInteger, primary_key=True)
    sender_id = Column(
        BigInteger,
        ForeignKey('users.user_id', ondelete='CASCADE')
    )
    receiver_id = Column(
        BigInteger,
        ForeignKey('users.user_id', ondelete='CASCADE')
    )

    query: sql.Select
