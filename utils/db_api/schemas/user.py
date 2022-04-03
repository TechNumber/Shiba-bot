from sqlalchemy import Column, Integer, BigInteger, String, sql, ForeignKey

from utils.db_api.db_gino import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)
    user_name = Column(String(100))
    shiba_name = Column(String(100))
    pic_url = Column(String(255))
    max_health = Column(Integer, default=100)
    health = Column(Integer, default=100)
    hunger = Column(Integer, default=100)
    money = Column(BigInteger, default=100)
    strength = Column(Integer, default=1)
    agility = Column(Integer, default=1)
    level = Column(Integer, default=1)
    exp = Column(Integer, default=0)
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
