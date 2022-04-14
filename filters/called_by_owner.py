from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery


class IsCalledByOwner(BoundFilter):
    """
    Данный фильтр обязателен к включению в список фильтров для обработчиков
    CallbackQuery, т.е. должен быть прописан внутри скобок декоратора среди
    прочих фильтров: @dp.callback_query_handler(IsCalledByOwner(), ...)

    Данный фильтр определяет, был ли кнопка (или другой вызывающий CallbackQuery объект)
    нажата тем же пользователем, который до этого инициировал появление этой самой кнопки.
    Фильтр необходим для того, чтобы другие пользователи не могли нажимать кнопки и
    производить действия в меню текущего пользователя. Это достигается за счёт того,
    что в обработчике, отвечающем за появление меню с кнопками, в CallbackData каждой
    кнопки записывается ID пользователя, для которого был вызван обработчик.
    """
    async def check(self, call: CallbackQuery) -> bool:
        """
        Данная функция проверяет, совпадает ли ID пользователя, для которого
        предназначалась кнопка, с ID пользователя, нажавшего на неё.

        Args:
            call (CallbackQuery): CallbackQuery, содержащий в CallbackData ID
            целевого пользователя

        Returns:
            (bool): True, если на кнопку нажал целевой пользователь, иначе False

        """
        owner_id = int((call.data.split(":"))[1])
        return call.from_user.id == owner_id
