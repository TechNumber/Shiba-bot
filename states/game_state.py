from aiogram.dispatcher.filters.state import StatesGroup, State


class GameState(StatesGroup):
    registered = State()
    shopping = State()
    naming = State()
