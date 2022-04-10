from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery


class IsCalledByOwner(BoundFilter):
    async def check(self, call: CallbackQuery) -> bool:
        owner_id = int((call.data.split(":"))[1])
        return call.from_user.id == owner_id
