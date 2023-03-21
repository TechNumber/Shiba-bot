import datetime
from typing import List

from aiogram import Dispatcher
from gino import Gino
import sqlalchemy as sa
from sqlalchemy import Column, DateTime

from data import config

db = Gino()


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.columns  # table.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimedBaseModel(BaseModel):
    """
    Является базовым абстрактным классом для всех таблиц в проекте.

    Columns:
         created_at (int): Дата и время создания записи в таблице.
         updated_at (int): Дата и время редактирования записи в таблице.
    """
    __abstract__ = True

    created_at = Column(DateTime(True), server_default=db.func.now())  # server_default — значение по умолчанию, kwargs
    updated_at = Column(DateTime(True),
                        default=db.func.now(),
                        onupdate=db.func.now(),
                        server_default=db.func.now())


async def on_startup(dispatcher: Dispatcher):
    print("Установка связи с PostgreSQL")
    await db.set_bind(config.POSTGRES_URI)
