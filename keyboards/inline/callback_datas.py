from aiogram.utils.callback_data import CallbackData

show_item_callback = CallbackData("show_item", "user_id", "item_type", "item_id")
buy_item_callback = CallbackData("buy_item", "user_id", "item_type", "item_id")
equip_item_callback = CallbackData("equip_item", "user_id", "item_type", "item_id")
discard_item_callback = CallbackData("discard_item", "user_id", "item_type", "item_id")
cancel_callback = CallbackData("cancel", "user_id", "cancel_type")
show_inventory_items_callback = CallbackData("show_inventory_items", "user_id", "item_type")
show_shop_items_callback = CallbackData("show_shop_items", "user_id", "item_type")
