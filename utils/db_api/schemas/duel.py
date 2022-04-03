from sqlalchemy import Column, Integer, sql, BigInteger, ForeignKey

from utils.db_api.db_gino import TimedBaseModel


class Duel(TimedBaseModel):
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
