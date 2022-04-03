from sqlalchemy import Column, Integer, sql, BigInteger, ForeignKey

from utils.db_api.db_gino import TimedBaseModel


class InventoryWeapon(TimedBaseModel):
    __tablename__ = 'inventory_weapons'
    entry_id = Column(BigInteger, primary_key=True)
    user_id = Column(
        BigInteger,
        ForeignKey('users.user_id', ondelete='CASCADE')
    )
    amount = Column(Integer)
    weapon_id = Column(
        Integer,
        ForeignKey('weapons.weapon_id', ondelete='CASCADE')
    )

    query: sql.Select
