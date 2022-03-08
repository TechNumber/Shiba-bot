# ПРОГРАММА ЗАПУСКАЕТСЯ ЕДИНОЖДЫ ДЛЯ ИНИЦИАЛИЗАЦИИ ТАБЛИЦЫ ЕДЫ

import asyncio

from data import config
from utils.db_api import food_commands
from utils.db_api.db_gino import db


async def food_init():
    await db.set_bind(config.POSTGRES_URI)
    await db.gino.drop_all()
    await db.gino.create_all()
    await food_commands.add_food(
        food_id=1, food_name="Сухой корм", food_price=25,
        food_description="Описание",
        food_chars="Описание через f строки с выгрузкой эффектов",
        max_health_time=0, max_health_add=0, max_health_mpy=1,
        health_time=0, health_add=20, health_mpy=1,
        strength_time=0, strength_add=0, strength_mpy=1
    )
    await food_commands.add_food(
        food_id=2, food_name="Говяжья кость", food_price=70,
        food_description="Описание",
        food_chars="Описание через f строки с выгрузкой эффектов",
        max_health_time=0, max_health_add=0, max_health_mpy=1,
        health_time=0, health_add=30, health_mpy=1,
        strength_time=5, strength_add=0, strength_mpy=1.2
    )
    await food_commands.add_food(
        food_id=3, food_name="Листик мяты", food_price=250,
        food_description="Описание",
        food_chars="Описание через f строки с выгрузкой эффектов",
        max_health_time=0, max_health_add=0, max_health_mpy=1,
        health_time=0, health_add=100, health_mpy=1,
        strength_time=0, strength_add=0, strength_mpy=1.5
    )
    await food_commands.add_food(
        food_id=4, food_name="Утиная грудка", food_price=200,
        food_description="Описание",
        food_chars="Описание через f строки с выгрузкой эффектов",
        max_health_time=0, max_health_add=0, max_health_mpy=1,
        health_time=0, health_add=100, health_mpy=1,
        strength_time=0, strength_add=0, strength_mpy=1
    )
    await food_commands.add_food(
        food_id=5, food_name="Каре ягненка", food_price=200,
        food_description="Описание",
        food_chars="Описание через f строки с выгрузкой эффектов",
        max_health_time=0, max_health_add=0, max_health_mpy=1,
        health_time=0, health_add=0, health_mpy=1,
        strength_time=5, strength_add=0, strength_mpy=2
    )
    await food_commands.add_food(
        food_id=6, food_name="Черная икра", food_price=1000,
        food_description="Описание",
        food_chars="Описание через f строки с выгрузкой эффектов",
        max_health_time=0, max_health_add=0, max_health_mpy=1,
        health_time=0, health_add=0, health_mpy=-1,  # коэффициент умножения -1 == полное восстановление здоровья
        strength_time=0, strength_add=0, strength_mpy=3
    )
    await food_commands.add_food(
        food_id=7, food_name="Фуа-гра", food_price=10000,
        food_description="Описание",
        food_chars="Описание через f строки с выгрузкой эффектов",
        max_health_time=0, max_health_add=1000, max_health_mpy=1,
        health_time=0, health_add=1000, health_mpy=1,
        strength_time=0, strength_add=0, strength_mpy=1
    )


loop = asyncio.get_event_loop()
loop.run_until_complete(food_init())
