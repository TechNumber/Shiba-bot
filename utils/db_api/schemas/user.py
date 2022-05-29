from sqlalchemy import Column, Integer, BigInteger, String, sql, ForeignKey
from sqlalchemy.orm import relationship, backref

from utils.db_api.db_gino import TimedBaseModel


class User(TimedBaseModel):
    """
    Таблица пользователей, участвующих в игре

    Columns:
        user_id (int, PK): ID пользователя в Telegram.
        user_name (str): Имя пользователя в Telegram.
        shiba_name (str): Имя собаки пользователя.
        pic_path (str): Адрес картинки собаки (персонажа) пользователя.
        max_health (int): Максимальное значение, которого может достигать здоровье
        игрока.
        health (int): Текущее значение здоровья игрока.
        hunger (int): Уровень голода собаки.
        money (int): Количество денег у игрока.
        strength (int): Значение силы игрока. Влияет на наносимый в сражениях урон.
        agility (int): Значение ловкости игрока. Влияет на шанс уклонения от атаки
        в сражениях.
        level (int): Уровень игрока. TODO: при повышении уровня можно увеличить один
        из основных показателей игрока на 1.
        exp (int): Количество опыта игрока. TODO: при накоплении достаточного количества
        очков опыта можно повысить уровень.
        weapon_id (int, FK): ID оружия, которое экипировал пользователь. Поле связано
        внешним ключом с полем weapon_id таблицы Weapon.
        outfit_id (int, FK): ID предмета одежды, который экипировал пользователь.
        Поле связано внешним ключом с полем outfit_id таблицы Outfit.
    """

    __tablename__ = 'users'

    inventory_weapons = relationship("InventoryWeapon", backref=backref("users", cascade='delete'),
                                     passive_deletes=True)
    inventory_outfits = relationship("InventoryOutfit", backref=backref("users", cascade='delete'),
                                     passive_deletes=True)
    inventory_meals = relationship("InventoryMeal", backref=backref("users", cascade='delete'),
                                   passive_deletes=True)
    duels = relationship("Duel", backref=backref("users", cascade='delete'),
                         passive_deletes=True)
    effects = relationship("Effect", backref=backref("users", cascade='delete'),
                           passive_deletes=True)
    user_id = Column(BigInteger, primary_key=True)
    user_name = Column(String(100))
    shiba_name = Column(String(100))
    pic_path = Column(String(255))
    max_health = Column(Integer, default=100)
    health = Column(Integer, default=100)
    hunger = Column(Integer, default=100)
    money = Column(BigInteger, default=200)
    strength = Column(Integer, default=1)
    agility = Column(Integer, default=1)
    level = Column(Integer, default=1)
    exp = Column(Integer, default=0)
    level_up = Column(Integer, default=0)
    weapon_id = Column(
        Integer,
        ForeignKey('weapons.weapon_id', ondelete='SET NULL'),
        nullable=True
    )
    outfit_id = Column(
        Integer,
        ForeignKey('outfits.outfit_id', ondelete='SET NULL'),
        nullable=True
    )

    query: sql.Select
