"""
В данном файле создаются экземпляры CallbackData(), которые передаются в качестве
CallbackData кнопок. Каждый экземпляр отвечает за свой тип кнопок и обладает
набором соответствующих полей для передачи информации внутри вызываемого кнопкой
CallbackQuery. В качестве данных CallbackQuery можно использовать строковые литералы,
но в этом случае возможны опечатки и путаница из-за отсутствия унификации.
"""

from aiogram.utils.callback_data import CallbackData

show_item_callback = CallbackData("show_item", "user_id", "item_type", "item_id")
buy_item_callback = CallbackData("buy_item", "user_id", "item_type", "item_id")
equip_item_callback = CallbackData("equip_item", "user_id", "item_type", "item_id")
discard_item_callback = CallbackData("discard_item", "user_id", "item_type", "item_id")
cancel_callback = CallbackData("cancel", "user_id", "cancel_type")
show_inventory_items_callback = CallbackData("show_inventory_items", "user_id", "item_type")
show_shop_items_callback = CallbackData("show_shop_items", "user_id", "item_type")
level_attribute_up_callback = CallbackData("level_attribute_up", "user_id", "attribute_type")
apply_level_up_callback = CallbackData("apply_level_up", "user_id")
