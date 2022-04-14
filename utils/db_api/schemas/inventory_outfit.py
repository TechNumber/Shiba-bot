from sqlalchemy import Column, Integer, sql, BigInteger, ForeignKey

from utils.db_api.db_gino import TimedBaseModel


class InventoryOutfit(TimedBaseModel):
    """
    Таблица, хранящая записи о том, какие предметы одежды находятся в инвентаре у
    пользователей и в каком количестве.

    Columns:
        entry_id (int, PK): ID записи о предмете одежды в инвентаре.
        user_id (int, FK): ID пользователя, которому принадлежит предмет одежды.
        Поле связано внешним ключом с полем user_id таблицы User.
        amount (int): Количество данного предмета одежды в инвентаре у пользователя.
        outfit_id (int, FK): ID предмета одежды. Поле связано внешним ключом с
        полем outfit_id таблицы Outfit.
    """
    __tablename__ = 'inventory_outfits'
    entry_id = Column(BigInteger, primary_key=True)
    user_id = Column(
        BigInteger,
        ForeignKey('users.user_id', ondelete='CASCADE')
    )
    amount = Column(Integer)
    outfit_id = Column(
        Integer,
        ForeignKey('outfits.outfit_id', ondelete='CASCADE')
    )

    query: sql.Select
