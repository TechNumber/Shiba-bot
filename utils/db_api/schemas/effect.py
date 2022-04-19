from sqlalchemy import Column, Integer, sql, BigInteger, ForeignKey
from utils.db_api.db_gino import TimedBaseModel


class Effect(TimedBaseModel):
    """
    Таблица, хранящая активные эффекты игроков.

    Columns:
        effect_id (int, PK): ID записи об активном эффекте.
        user_id (int, FK): ID пользователя, на которого действует эффект.
        Поле связано внешним ключом с полем user_id таблицы User.
        meal_id (int, FK): ID предмета еды, который даровал эффект.
        Поле связано внешним ключом с полем meal_id таблицы Meal.
        max_health_duration (int): Оставшееся время действия эффекта
        увеличения макс. здоровья в дуэлях. -1, если эффект перманентный
        health_duration (int): Оставшееся время действия эффекта
        увеличения текущего здоровья в дуэлях. -1, если эффект перманентный
        strength_duration (int): Оставшееся время действия эффекта
        увеличения силы в дуэлях. -1, если эффект перманентный
        agility_duration (int): Оставшееся время действия эффекта
        увеличения ловкости в дуэлях. -1, если эффект перманентный
    """


    __tablename__ = 'effects'
    effect_id = Column(BigInteger, primary_key=True)
    user_id = Column(
        BigInteger,
        ForeignKey('users.user_id', ondelete='CASCADE')
    )
    meal_id = Column(
        BigInteger,
        ForeignKey('meals.meal_id', ondelete='CASCADE')
    )
    max_health_duration = Column(Integer)  # Время действия эффекта в дуэлях. -1, если эффект перманентный
    health_duration = Column(Integer)  # Время действия эффекта в дуэлях. -1, если эффект перманентный
    strength_duration = Column(Integer)  # Время действия эффекта в дуэлях. -1, если эффект перманентный
    agility_duration = Column(Integer)  # Время действия эффекта в дуэлях. -1, если эффект перманентный
    query: sql.Select
