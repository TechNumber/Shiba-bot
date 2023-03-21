from sqlalchemy import Column, Integer, sql, BigInteger, ForeignKey

from utils.db_api.db_gino import TimedBaseModel


class InventoryWeapon(TimedBaseModel):
    """
    Таблица, хранящая записи о том, какое оружие находятся в инвентаре у
    пользователей и в каком количестве.

    Columns:
        entry_id (int, PK): ID записи об оружии в инвентаре.
        user_id (int, FK): ID пользователя, которому принадлежит оружие. Поле
        связано внешним ключом с полем user_id таблицы User.
        amount (int): Количество данного оружия в инвентаре у пользователя.
        weapon_id (int, FK): ID оружия. Поле связано внешним ключом с полем
        weapon_id таблицы Weapon.
    """
    __tablename__ = 'inventory_weapons'
    entry_id = Column(BigInteger, primary_key=True)
    user_id = Column(
        BigInteger,
        ForeignKey('users.user_id', ondelete='CASCADE')
    )
    amount = Column(Integer)
    weapon_id = Column(
        Integer,
        ForeignKey('weapons.weapon_id', ondelete='CASCADE')
    )

    query: sql.Select
