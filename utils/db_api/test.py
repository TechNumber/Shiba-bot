import asyncio

from asyncpg import UndefinedTableError

from data import config
from utils.db_api import user_commands, all_init, duel_commands, inventory_outfit_commands
from utils.db_api.db_gino import db
from utils.db_api.schemas.duel import Duel
from utils.db_api.schemas.inventory_outfit import InventoryOutfit
from utils.db_api.schemas.user import User
from utils.db_api.schemas.weapon import Weapon
from utils.db_api.schemas.inventory_weapon import InventoryWeapon
from utils.db_api import inventory_weapon_commands


async def test():
    await db.set_bind(config.POSTGRES_URI)
    try:
        await Duel.__table__.gino.drop()
    except UndefinedTableError:
        pass
    try:
        await InventoryWeapon.__table__.gino.drop()
    except UndefinedTableError:
        pass
    try:
        await InventoryOutfit.__table__.gino.drop()
    except UndefinedTableError:
        pass
    try:
        await User.__table__.gino.drop()
    except UndefinedTableError:
        pass
    await all_init.all_init()
    await User.__table__.gino.create()
    await InventoryOutfit.__table__.gino.create()
    await InventoryWeapon.__table__.gino.create()
    await Duel.__table__.gino.create()
    print("Добавляем пользователей")
    await user_commands.add_user(1, "One", "email")
    await user_commands.add_user(2, "Vasya", "vv@gmail.com")
    await user_commands.add_user(3, "1", "1")
    await user_commands.add_user(4, "1", "1")
    await user_commands.add_user(5, "John", "john@mail.com")
    await user_commands.add_user(
        user_id=6,
        user_name="Antony",
        shiba_name="Max",
        weapon_id=1,
        outfit_id=1,
    )
    await user_commands.add_user(
        user_id=7,
        user_name="Michael",
        shiba_name="Spark",
        weapon_id=2,
        outfit_id=2,
    )
    await user_commands.add_user(
        user_id=8,
        user_name="Tanya",
        shiba_name="Daniel",
        weapon_id=3,
        outfit_id=3,
    )
    print("Готово")

    # users = list(map(str, await user_commands.select_all_users()))
    # print(f"Получил всех пользователей: {users}")

    # count_users = await user_commands.count_users()
    # print(f"Всего пользователей: {count_users}")

    # user = await user_commands.select_user(user_id=5)
    # print(f"Получил пользователя: {user}")

    # await user_commands.update_shiba_name(5, "etoighjworetihj@wef.gh")
    # id_list = await user_commands.get_all_users_id()
    # print(id_list)
    await inventory_weapon_commands.add_inventory_weapon(1, 1)
    await inventory_outfit_commands.add_inventory_outfit(1, 1)
    await inventory_weapon_commands.add_inventory_weapon(1, 1)
    await inventory_outfit_commands.add_inventory_outfit(1, 1)

    await inventory_weapon_commands.discard_inventory_weapon(1, 1)
    await inventory_outfit_commands.discard_inventory_outfit(1, 1)
    await inventory_weapon_commands.discard_inventory_weapon(1, 1)
    await inventory_outfit_commands.discard_inventory_outfit(1, 1)
    await inventory_weapon_commands.discard_inventory_weapon(1, 1)
    await inventory_outfit_commands.discard_inventory_outfit(1, 1)

    user = await User.query.where(User.user_id == 6).gino.first()
    print(user)
    weapon = await Weapon.query.where(Weapon.weapon_id == 1).gino.first()
    await weapon.delete()
    user = await User.query.where(User.user_id == 6).gino.first()
    print(user)

    await duel_commands.add_duel(sender_id=6, receiver_id=7)
    await duel_commands.add_duel(sender_id=8, receiver_id=7)
    await duel_commands.add_duel(sender_id=7, receiver_id=6)
    id_list = await duel_commands.select_all_senders_id(receiver_id=7)
    print(id_list)

    user = await User.query.where(User.user_id == 6).gino.first()
    await user.delete()

    print()


loop = asyncio.get_event_loop()
loop.run_until_complete(test())
