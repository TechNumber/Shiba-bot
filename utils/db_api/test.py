import asyncio

from data import config
from utils.db_api import user_commands
from utils.db_api.db_gino import db
from utils.db_api.schemas.user import User
from utils.db_api.schemas.inventory_weapon import InventoryWeapon
from utils.db_api import inventory_weapon_commands


async def test():
    await db.set_bind(config.POSTGRES_URI)
    await User.__table__.gino.drop()
    await User.__table__.gino.create()
    await InventoryWeapon.__table__.gino.drop()
    await InventoryWeapon.__table__.gino.create()
    print("Добавляем пользователей")
    await user_commands.add_user(1, "One", "email")
    await user_commands.add_user(2, "Vasya", "vv@gmail.com")
    await user_commands.add_user(3, "1", "1")
    await user_commands.add_user(4, "1", "1")
    await user_commands.add_user(5, "John", "john@mail.com")
    print("Готово")

    users = list(map(str, await user_commands.select_all_users()))
    print(f"Получил всех пользователей: {users}")

    count_users = await user_commands.count_users()
    print(f"Всего пользователей: {count_users}")

    user = await user_commands.select_user(user_id=5)
    print(f"Получил пользователя: {user}")

    await user_commands.update_shiba_name(5, "etoighjworetihj@wef.gh")

    await inventory_weapon_commands.add_inventory_weapon(12435134, 1)
    await inventory_weapon_commands.discard_inventory_weapon(12435134, 1)
    print()


loop = asyncio.get_event_loop()
loop.run_until_complete(test())
