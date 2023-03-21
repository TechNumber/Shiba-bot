from sqlalchemy import Column, Integer, Float, String, sql
from sqlalchemy.orm import relationship, backref

from utils.db_api.db_gino import TimedBaseModel


class Outfit(TimedBaseModel):
    """
    Таблица, хранящая присутствующие в игре предметы одежды.

    Columns:
        outfit_id (int, PK): ID записи о предмете одежды.
        outfit_name (str): Название предмета одежды.
        outfit_price (str): Стоимость предмета одежды.
        outfit_description (str): Словесное описание предмета одежды.
        outfit_chars (str): Список эффектов предмета одежды.
        health_add (int): На сколько единиц увеличивается текущее здоровье.
        health_mpy (float): Во сколько раз увеличивается текущее здоровье.
        agility_add (int): На сколько единиц увеличивается ловкость.
        agility_mpy (float): Во сколько раз увеличивается ловкость.
        strength_add (int): На сколько единиц увеличивается сила.
        strength_mpy (float): Во сколько раз увеличивается сила.
    """
    __tablename__ = 'outfits'
    outfit_id = Column(Integer, primary_key=True)

    inventory_outfits = relationship("InventoryOutfit", backref=backref("outfits", cascade='delete'),
                                     passive_deletes=True)
    users = relationship("User", backref=backref("outfits", cascade='delete'), passive_deletes=True)

    outfit_name = Column(String(100))
    outfit_price = Column(Integer)
    outfit_description = Column(String(255))
    outfit_chars = Column(String(1000))
    health_add = Column(Integer)  # На сколько единиц увеличивается текущее здоровье
    health_mpy = Column(Float)  # Во сколько раз увеличивается текущее здоровье
    agility_add = Column(Integer)  # На сколько единиц увеличивается ловкость
    agility_mpy = Column(Float)  # Во сколько раз увеличивается ловкость
    strength_add = Column(Integer)  # На сколько единиц увеличивается сила
    strength_mpy = Column(Float)  # Во сколько раз увеличивается сила

    query: sql.Select
