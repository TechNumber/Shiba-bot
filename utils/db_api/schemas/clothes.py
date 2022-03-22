from sqlalchemy import Column, Integer, Float, String, sql

from utils.db_api.db_gino import TimedBaseModel


class Clothes(TimedBaseModel):
    __tablename__ = 'clothes'
    clothes_id = Column(Integer, primary_key=True)
    clothes_name = Column(String(100))
    clothes_price = Column(Integer)
    clothes_description = Column(String(255))
    clothes_chars = Column(String(255))
    health_add = Column(Integer)  # На сколько единиц увеличивается текущее здоровье
    health_mpy = Column(Float)  # Во сколько раз увеличивается текущее здоровье
    agility_add = Column(Integer)  # На сколько единиц увеличивается ловкость
    agility_mpy = Column(Float)  # Во сколько раз увеличивается ловкость
    strength_add = Column(Integer)  # На сколько единиц увеличивается сила
    strength_mpy = Column(Float)  # Во сколько раз увеличивается сила

    query: sql.Select
