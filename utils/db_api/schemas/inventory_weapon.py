from sqlalchemy import Column, Integer, Float, String, sql, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from utils.db_api.db_gino import TimedBaseModel


class InventoryWeapon(TimedBaseModel):
    __tablename__ = 'inventory_weapons'
    entry_id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    amount = Column(Integer)
    weapon_id = Column(
        Integer,
        ForeignKey('weapons.weapon_id', ondelete='SET NULL')
    )
    weapon = relationship("Weapon")

    query: sql.Select
