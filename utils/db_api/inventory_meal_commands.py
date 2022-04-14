from asyncpg import UniqueViolationError
from sqlalchemy import and_
import hashlib

from utils.db_api import meal_commands
from utils.db_api.schemas.inventory_meal import InventoryMeal


async def add_inventory_meal(user_id: int,
                             meal_id: int):
    """
    Вносит запись о том, что в инвентарь пользователя с ID user_id было добавлено блюдо
    с ID meal_id.

    Args:
        user_id: ID пользователя, в инвентарь которого добавляется блюдо.
        meal_id: ID блюда, которое добавляется в инвентарь пользователя.

    Returns:
        None
    """
    try:
        inventory_meal = InventoryMeal(
            entry_id=int(hashlib.sha256((str(user_id) + str(meal_id)).encode('utf-8')).hexdigest(), 16) % 10 ** 8,
            user_id=user_id,
            amount=1,
            meal_id=meal_id
        )
        await inventory_meal.create()

    except UniqueViolationError:
        inventory_meal = await InventoryMeal.query.where(
            and_(
                InventoryMeal.user_id == user_id,
                InventoryMeal.meal_id == meal_id
            )
        ).gino.first()
        await inventory_meal.update(amount=inventory_meal.amount + 1).apply()


async def discard_inventory_meal(user_id: int,
                                 meal_id: int):
    """
    Удаляет блюдо с ID meal_id из инвентаря пользователя с ID user_id.
    Если блюдо находится в инвентаре в количестве, большем 1, количество этого
    блюда в записи понижается на 1. Если количество равно 1, запись удаляется
    из таблицы. Если такого блюда нет в инвентаре указанного игрока, в консоль
    выводится сообщение о том, что запись не найдена.

    Args:
        user_id (int): ID пользователя, из инвентаря которого удаляется блюдо.
        meal_id (int): ID блюда, которое удаляется из инвентаря пользователя.

    Returns:
        None
    """
    inventory_meal = await InventoryMeal.query.where(
        and_(
            InventoryMeal.user_id == user_id,
            InventoryMeal.meal_id == meal_id
        )
    ).gino.first()
    if inventory_meal is not None:
        if inventory_meal.amount > 1:
            await inventory_meal.update(amount=inventory_meal.amount - 1).apply()
        else:
            await inventory_meal.delete()
    else:
        print("Запись не найдена")


async def select_all_meals_by_user_id(user_id: int):
    """
    Возвращает записи о блюдах, которые находятся в инвентаре пользователя с ID
    user_id.

    Args:
        user_id:

    Returns:

    """
    entries = await InventoryMeal.query.where(
        InventoryMeal.user_id == user_id
    ).gino.all()
    meals = [await meal_commands.select_meal(entry.meal_id) for entry in entries]
    return meals


async def get_meal_amount(user_id: int, meal_id: int):
    entry = await InventoryMeal.query.where(
        and_(
            InventoryMeal.user_id == user_id,
            InventoryMeal.meal_id == meal_id
        )
    ).gino.first()
    return entry.amount
