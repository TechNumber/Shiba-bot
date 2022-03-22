from sqlalchemy import Column, Integer, Float, String, sql

from utils.db_api.db_gino import TimedBaseModel


class Outfit(TimedBaseModel):
    __tablename__ = 'outfits'
    outfit_id = Column(Integer, primary_key=True)
    outfit_name = Column(String(100))
    outfit_price = Column(Integer)
    outfit_description = Column(String(255))
    outfit_chars = Column(String(255))
    health_add = Column(Integer)  # На сколько единиц увеличивается текущее здоровье
    health_mpy = Column(Float)  # Во сколько раз увеличивается текущее здоровье
    agility_add = Column(Integer)  # На сколько единиц увеличивается ловкость
    agility_mpy = Column(Float)  # Во сколько раз увеличивается ловкость
    strength_add = Column(Integer)  # На сколько единиц увеличивается сила
    strength_mpy = Column(Float)  # Во сколько раз увеличивается сила

    query: sql.Select
