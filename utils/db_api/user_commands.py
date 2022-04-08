from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.schemas.user import User


async def add_user(user_id: int,
                   user_name: str,
                   shiba_name: str = None,
                   pic_url: str = None,
                   weapon_id: int = None,
                   outfit_id: int = None):
    try:
        user = User(
            user_id=user_id,
            user_name=user_name,
            shiba_name=shiba_name,
            pic_url=pic_url,
            weapon_id=weapon_id,
            outfit_id=outfit_id
        )
        await user.create()

    except UniqueViolationError:
        pass


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def select_user(user_id: int):
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user


async def count_users():
    total = await db.func.count(User.user_id).gino.scalar()
    return total


async def update_shiba_name(user_id, shiba_name):
    user = await User.get(user_id)
    await user.update(shiba_name=shiba_name).apply()


async def update_user_money(user_id, money):
    user = await User.get(user_id)
    await user.update(money=money).apply()


async def get_all_users_id():
    user_id_list = await User.query.gino.load(User.user_id).all()
    return user_id_list
