# ---------------------------------------------------------------------------------
# В данном файле проводилось тестирование временных изменений в базе данных:
# в таблице обновляется поле, после чего, через некоторый промежуток времени,
# поле возвращается в исходное состояние. Это необходимо для временных эффектов у
# предметов. Пока трудно сказать, является ли представленное ниже решение
# с созданием "задач" и их конкурентным (параллельным) запуском через метод gather
# надлежащим решением. Метод gather передаёт управление задачам, тем самым
# приостанавливая выполнение функции, из которой он был вызван. Как поведёт себя
# итоговый код проекта при использовании такого подхода станет ясно, когда дело
# дойдёт непосредственно до реализации функций использования предметов. Пока же
# оставляю этот код здесь. Если в конечном счёте решение окажется непригодным,
# то, скорее всего, придётся прибегнуть к multiprocessing.
# ---------------------------------------------------------------------------------


import asyncio
import time

from data import config
from utils.db_api import user_commands
from utils.db_api.db_gino import db
from utils.db_api.schemas.user import User


async def delay():
    user = await user_commands.select_user(user_id=1)
    await asyncio.sleep(5)
    await user.update(level=user.level - 10).apply()
    print(f"Получил пользователя: {user}")


async def increase():
    user = await user_commands.select_user(user_id=1)
    await user.update(level=user.level + 10).apply()
    print(f"Получил пользователя: {user}")


async def test():
    await db.set_bind(config.POSTGRES_URI)
    await User.__table__.gino.drop()
    await User.__table__.gino.create()
    await user_commands.add_user(1, "John", "Shiba")
    tasks = [
        increase(),
        delay()
    ]
    await asyncio.gather(*tasks)
    await user_commands.add_user(2, "Sam", "Corgi")


loop = asyncio.get_event_loop()
loop.run_until_complete(test())
