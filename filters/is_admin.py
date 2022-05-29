from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

import data.config


class IsAdmin(BoundFilter):
    async def check(self, message: Message) -> bool:
        admins = data.config.ADMINS
        ok = any(str(message.from_user.id) == admin for admin in admins)
        return ok


