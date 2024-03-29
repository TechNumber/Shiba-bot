from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message


class IsChat(BoundFilter):
    async def check(self, message: Message) -> bool:
        return message.chat.type == types.ChatType.PRIVATE
