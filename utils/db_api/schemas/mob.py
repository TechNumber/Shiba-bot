from sqlalchemy import Column, Integer, BigInteger, String, sql, ForeignKey
from sqlalchemy.orm import relationship, backref

from utils.db_api.db_gino import TimedBaseModel


class Mob(TimedBaseModel):
    """
    Таблица мобов, которых можно встретить в данже

    Columns:
        mob_id (int, PK): ID моба.
        mob_name (str): Название моба.
        mob_description (str): Описание моба.
        mob_chars (str): Описание характеристик моба.
        mob_pic_url (str): Адрес картинки моба.
        mob_health (int): Запас здоровья моба.
        mob_strength (int): Значение силы моба. Влияет на наносимый в сражениях урон.
        mob_agility (int): Значение ловкости моба. Влияет на шанс уклонения от атаки
        в сражениях.
        mob_level (int): Уровень игрока. TODO: при повышении уровня можно увеличить один
        из основных показателей игрока на 1.
        TODO: как-то связать с уровнем игрока
    """

    __tablename__ = 'mobs'

    mob_id = Column(BigInteger, primary_key=True)
    mob_name = Column(String(100))
    mob_description = Column(String(255))
    mob_chars = Column(String(1000), default="")
    mob_pic_url = Column(String(255), default="")
    mob_health = Column(Integer, default=1)
    mob_strength = Column(Integer, default=1)
    mob_agility = Column(Integer, default=1)
    mob_level = Column(Integer, default=1)

    query: sql.Select
