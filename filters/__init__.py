from aiogram import Dispatcher

from loader import dp

# from .is_admin import AdminFilter
from .called_by_owner import IsCalledByOwner

if __name__ == "filters":
    dp.filters_factory.bind(IsCalledByOwner)
