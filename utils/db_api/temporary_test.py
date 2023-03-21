# ------------------------------------------------------------------------------------
# UPD: в реализации временных эффектов через счётчик дуэлей и таблицу хранения
# коэффициентов умножения и добавления подход с asyncio.sleep, представленный ниже,
# не используется.
#
# В данном файле проводилось тестирование временных изменений в базе данных:
# в таблице обновляется поле, после чего, через некоторый промежуток времени,
# поле возвращается в исходное состояние. Это необходимо для временных эффектов у
# предметов. Пока трудно сказать, является ли представленное ниже решение
# с созданием "задач" и их конкурентным (параллельным) запуском через метод gather
# надлежащим решением. Метод gather передаёт управление задачам, тем самым
# приостанавливая выполнение функции, из которой он был вызван. Как поведёт себя
# итоговый код проекта при использовании такого подхода станет ясно, когда дело
# дойдёт непосредственно до реализации функций использования предметов.
# (UPD: метод действительно сработал, выполнение программы не останавливалось,
# если из обработчика кнопки "Съесть" конкурентно вызывались обработчики eat_meal,
# discard_meal и обработчик возвращение в меню выбора еды. А в самом eat_meal
# конкурентно вызывались функции увеличения показателей и их последующего понижения
# по прошествии указанного времени. Однако, как уже говорилось в обновлении выше,
# теперь этот подход не используется).
# ------------------------------------------------------------------------------------


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
