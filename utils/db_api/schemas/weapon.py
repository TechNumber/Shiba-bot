from sqlalchemy import Column, Integer, Float, String, sql
from sqlalchemy.orm import relationship, backref

from utils.db_api.db_gino import TimedBaseModel


class Weapon(TimedBaseModel):
    """
    Таблица, хранящая присутствующее в игре оружие.

    Columns:
        weapon_id (int, PK): ID записи об оружии.
        weapon_name (str): Название оружия.
        weapon_price (str): Стоимость оружия.
        weapon_description (str): Словесное описание оружия.
        weapon_chars (str): Список эффектов оружия.
        damage (int): Количество наносимого урона.
        health_add (int): На сколько единиц увеличивается текущее здоровье.
        health_mpy (float): Во сколько раз увеличивается текущее здоровье.
        agility_add (int): На сколько единиц увеличивается ловкость.
        agility_mpy (float): Во сколько раз увеличивается ловкость.
    """
    __tablename__ = 'weapons'
    weapon_id = Column(Integer, primary_key=True)

    inventory_weapons = relationship("InventoryWeapon", backref=backref("weapons", cascade='delete'),
                                     passive_deletes=True)
    users = relationship("User", backref=backref("weapons", cascade='delete'), passive_deletes=True)

    weapon_name = Column(String(100))
    weapon_price = Column(Integer)
    weapon_description = Column(String(255))
    weapon_chars = Column(String(1000))
    damage = Column(Integer)  # Сколько урона наносит
    agility_add = Column(Integer)  # На сколько единиц увеличивается ловкость
    agility_mpy = Column(Float)  # Во сколько раз увеличивается ловкость
    health_add = Column(Integer)  # На сколько единиц увеличивается текущее здоровье
    health_mpy = Column(Float)  # Во сколько раз увеличивается текущее здоровье

    query: sql.Select
