from sqlalchemy import Column, Integer, sql, BigInteger, ForeignKey

from utils.db_api.db_gino import TimedBaseModel


class InventoryMeal(TimedBaseModel):
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
