from sqlalchemy import Column, Integer, sql, BigInteger, ForeignKey

from utils.db_api.db_gino import TimedBaseModel


class InventoryOutfit(TimedBaseModel):
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
