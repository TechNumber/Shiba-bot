from aiogram.utils.callback_data import CallbackData

choose_item_callback = CallbackData("choose_item", "item_type", "item_id")
buy_item_callback = CallbackData("buy_item", "item_type", "item_id")
