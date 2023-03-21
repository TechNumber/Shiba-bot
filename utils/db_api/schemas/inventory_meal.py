from sqlalchemy import Column, Integer, sql, BigInteger, ForeignKey

from utils.db_api.db_gino import TimedBaseModel


class InventoryMeal(TimedBaseModel):
    """
    Таблица, хранящая записи о том, какие блюда находятся в инвентаре у пользователей
    и в каком количестве.

    Columns:
        entry_id (int, PK): ID записи о блюде в инвентаре.
        user_id (int, FK): ID пользователя, которому принадлежит блюдо. Поле
        связано внешним ключом с полем user_id таблицы User.
        amount (int): Количество данного блюда в инвентаре у пользователя.
        meal_id (int, FK): ID блюда. Поле связано внешним ключом с полем meal_id
        таблицы Meal.
    """
    __tablename__ = 'inventory_meals'
    entry_id = Column(BigInteger, primary_key=True)
    user_id = Column(
        BigInteger,
        ForeignKey('users.user_id', ondelete='CASCADE')
    )
    amount = Column(Integer)
    meal_id = Column(
        Integer,
        ForeignKey('meals.meal_id', ondelete='CASCADE')
    )

    query: sql.Select

# TODO: добавить ограничение по количеству предметов в инвентаре
