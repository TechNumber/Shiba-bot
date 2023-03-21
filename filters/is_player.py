from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from utils.db_api import user_commands


class IsPlayer(BoundFilter):
    async def check(self, message: Message) -> bool:
        ok = message.from_user.id in await user_commands.get_all_users_id()
        return ok
