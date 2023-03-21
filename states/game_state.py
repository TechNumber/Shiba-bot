from aiogram.dispatcher.filters.state import StatesGroup, State


class GameState(StatesGroup):
    """
    Данный класс содержит в себе состояния, в которых может находиться игрок в течение
    игры. Это позволяет перенаправлять update в подходящие обработчики в зависимости
    от состояния, в котором находится пользователь. В частности, это защищает от ситуаций,
    когда пользователь пытается выполнить действие, находясь в процессе выполнения другого
    действия (Попытка вызвать другого игрока на дуэль, находясь в состоянии shopping).
    """
    registered = State()
    shopping = State()
    inventory = State()
    naming = State()
    level_up = State()
    choosing_picture = State()
