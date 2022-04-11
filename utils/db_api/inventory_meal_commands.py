from asyncpg import UniqueViolationError
from sqlalchemy import and_
import hashlib

from utils.db_api import meal_commands
from utils.db_api.schemas.inventory_meal import InventoryMeal


async def add_inventory_meal(user_id: int,
                             meal_id: int):
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

