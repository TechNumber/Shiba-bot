from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.schemas.user import User


async def add_user(user_id: int, user_name: str, shibu_name: str = None, pic_url: str = None):
    try:
        user = User(user_id=user_id, user_name=user_name, shibu_name=shibu_name, pic_url=pic_url)
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


async def update_shibu_name(user_id, shibu_name):
    user = await User.get(user_id)
    await user.update(shibu_name=shibu_name).apply()
