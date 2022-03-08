from sqlalchemy import Column, Integer, BigInteger, String, sql

from utils.db_api.db_gino import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)
    user_name = Column(String(100))
    shibu_name = Column(String(100))
    pic_url = Column(String(255))
    weapon_id = Column(Integer) #Внешний ключ
    clothes_id = Column(Integer) #Внешний ключ
    health = Column(Integer, default=100)
    hunger = Column(Integer, default=100)
    money = Column(BigInteger, default=100)
    strength = Column(Integer, default=1)
    agility = Column(Integer, default=1)
    level = Column(Integer, default=1)
    exp = Column(Integer, default=0)

    query: sql.Select
