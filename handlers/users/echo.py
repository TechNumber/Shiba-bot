from aiogram import types
from aiogram.dispatcher import FSMContext

from filters.is_chat import IsChat
from loader import dp


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_handler(IsChat(), state=None)
async def bot_echo(message: types.Message):
    await message.answer("Игровые команды бота доступны только в групповом чате и только присоединившимся игрокам.")
    # await message.answer(f"Эхо без состояния."
    #                      f"Сообщение:\n"
    #                      f"{message.text}")


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
@dp.message_handler(IsChat(), state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    await message.answer("Игровые команды бота доступны только в групповом чате и только присоединившимся игрокам.")
    # state = await state.get_state()
    # await message.answer(f"Эхо в состоянии <code>{state}</code>.\n"
    #                      f"\nСодержание сообщения:\n"
    #                      f"<code>{message}</code>")
