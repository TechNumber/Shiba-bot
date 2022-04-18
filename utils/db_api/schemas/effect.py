from sqlalchemy import Column, Integer, sql, BigInteger, ForeignKey
from utils.db_api.db_gino import TimedBaseModel


class Effect(TimedBaseModel):
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
    agility_duration = Column(Integer)  # Длительность баффа ловкости в дуэлях
    query: sql.Select
