from aiogram import Dispatcher

from loader import dp

# from .is_admin import AdminFilter
from .called_by_owner import IsCalledByOwner
from .is_player import IsPlayer
from .is_chat import IsChat

if __name__ == "filters":
    dp.filters_factory.bind(IsCalledByOwner)
    dp.filters_factory.bind(IsPlayer)
    dp.filters_factory.bind(IsChat)
