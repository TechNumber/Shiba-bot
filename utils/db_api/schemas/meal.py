from sqlalchemy import Column, Integer, Float, String, sql
from sqlalchemy.orm import relationship, backref

from utils.db_api.db_gino import TimedBaseModel


class Meal(TimedBaseModel):
    """
    Таблица, хранящая присутствующие в игре блюда.

    Columns:
        meal_id (int, PK): ID записи о блюде.
        meal_name (str): Название блюда.
        meal_price (str): Стоимость блюда.
        meal_description (str): Словесное описание блюда.
        meal_chars (str): Список эффектов блюда.
        max_health_time (float): Время действия эффекта в минутах. 0,  если эффект перманентный.
        max_health_add (int): На сколько единиц увеличивается максимальное здоровье.
        max_health_mpy (float): Во сколько раз увеличивается максимальное здоровье.
        health_time (float): Время действия эффекта в минутах. 0, если эффект перманентный.
        health_add (int): На сколько единиц увеличивается текущее здоровье.
        health_mpy (float): Во сколько раз увеличивается текущее здоровье.
        strength_time (float): Время действия эффекта в минутах. 0, если эффект перманентный.
        strength_add (int): На сколько единиц увеличивается сила.
        strength_mpy (float): Во сколько раз увеличивается сила.
    """

    __tablename__ = 'meals'

    inventory_meals = relationship("InventoryMeal", backref=backref("meals", cascade='delete'),
                                   passive_deletes=True)
    effects = relationship("Meal", backref=backref("effects", cascade='delete'),
                           passive_deletes=True)
    meal_id = Column(Integer, primary_key=True)
    meal_name = Column(String(100))  # Название
    meal_price = Column(Integer)  # Стоимость
    meal_description = Column(String(255))  # Словесное описание
    meal_chars = Column(String(1000))  # Список эффектов
    max_health_time = Column(Integer)  # Время действия эффекта в дуэлях. 0, если эффект перманентный
    max_health_add = Column(Integer)  # На сколько единиц увеличивается максимальное здоровье
    max_health_mpy = Column(Float)  # Во сколько раз увеличивается максимальное здоровье
    health_time = Column(Integer)  # Время действия эффекта в дуэлях. 0, если эффект перманентный
    health_add = Column(Integer)  # На сколько единиц увеличивается текущее здоровье
    health_mpy = Column(Float)  # Во сколько раз увеличивается текущее здоровье
    strength_time = Column(Integer)  # Время действия эффекта в дуэлях. 0, если эффект перманентный
    strength_add = Column(Integer)  # На сколько единиц увеличивается сила
    strength_mpy = Column(Float)  # Во сколько раз увеличивается сила
    agility_time = Column(Integer)  # Длительность баффа ловкости в дуэлях
    agility_add = Column(Integer)  # Увеличение ловкости на n ед.
    agility_mpy = Column(Float)  # Множитель баффа ловкости

    query: sql.Select
