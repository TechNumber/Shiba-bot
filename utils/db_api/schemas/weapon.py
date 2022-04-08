from sqlalchemy import Column, Integer, Float, String, sql
from sqlalchemy.orm import relationship, backref

from utils.db_api.db_gino import TimedBaseModel


class Weapon(TimedBaseModel):
    __tablename__ = 'weapons'
    weapon_id = Column(Integer, primary_key=True)

    inventory_weapons = relationship("InventoryWeapon", backref=backref("weapons", cascade='delete'),
                                     passive_deletes=True)
    users = relationship("User", backref=backref("weapons", cascade='delete'), passive_deletes=True)

    weapon_name = Column(String(100))
    weapon_price = Column(Integer)
    weapon_description = Column(String(255))
    weapon_chars = Column(String(255))
    damage = Column(Integer)  # Сколько урона наносит
    agility_add = Column(Integer)  # На сколько единиц увеличивается ловкость
    agility_mpy = Column(Float)  # Во сколько раз увеличивается ловкость
    health_add = Column(Integer)  # На сколько единиц увеличивается текущее здоровье
    health_mpy = Column(Float)  # Во сколько раз увеличивается текущее здоровье

    query: sql.Select
