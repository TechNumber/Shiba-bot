from sqlalchemy import Column, Integer, Float, String, sql

from utils.db_api.db_gino import TimedBaseModel


class Food(TimedBaseModel):
    __tablename__ = 'food'
    food_id = Column(Integer, primary_key=True)
    food_name = Column(String(100))  # Название
    food_price = Column(Integer)  # Стоимость
    food_description = Column(String(255))  # Словесное описание
    food_chars = Column(String(255))  # Список эффектов
    # эффекты максимального здоровья — избыточный атрибут,
    # занимает три столбца, надо бы чем-то заменить
    max_health_time = Column(Integer)  # Время действия эффекта в минутах. 0, если эффект перманентный
    max_health_add = Column(Integer)  # На сколько единиц увеличивается максимальное здоровье
    max_health_mpy = Column(Float)  # Во сколько раз увеличивается максимальное здоровье
    health_time = Column(Integer)  # Время действия эффекта в минутах. 0, если эффект перманентный
    health_add = Column(Integer)  # На сколько единиц увеличивается текущее здоровье
    health_mpy = Column(Float)  # Во сколько раз увеличивается текущее здоровье
    strength_time = Column(Integer)  # Время действия эффекта в минутах. 0, если эффект перманентный
    strength_add = Column(Integer)  # На сколько единиц увеличивается сила
    strength_mpy = Column(Float)  # Во сколько раз увеличивается сила

    query: sql.Select
