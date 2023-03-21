import pathlib

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import InputFile

from keyboards.inline.my_shiba.my_shiba_menus import get_my_shiba_menu
from loader import dp
from states.game_state import GameState
from utils.db_api import user_commands, weapon_commands, outfit_commands, effect_commands, meal_commands


@dp.message_handler(Command("my_shiba"), state=GameState.registered)
async def show_my_shiba_menu(message: types.Message):
    if message.from_user.username is not None:
        sender_link = f"<a href=\"t.me/{message.from_user.username}\">{message.from_user.username}</a>"
    else:
        sender_link = f"<a href=\"tg://user?id={message.from_user.id}\">{message.from_user.full_name}</a>"
    user = await user_commands.select_user(message.from_user.id)
    total_max_health_add = total_strength_add = total_agility_add = 0
    total_max_health_mpy = total_strength_mpy = total_agility_mpy = 1
    if user.weapon_id is not None:
        weapon = await weapon_commands.select_weapon(user.weapon_id)
        weapon_name = weapon.weapon_name
        total_max_health_add += weapon.health_add
        total_max_health_mpy *= weapon.health_mpy
        total_agility_add += weapon.agility_add
        total_agility_mpy *= weapon.agility_mpy
    else:
        weapon_name = "нет"
    if user.outfit_id is not None:
        outfit = await outfit_commands.select_outfit(user.outfit_id)
        outfit_name = outfit.outfit_name
        total_max_health_add += outfit.health_add
        total_max_health_mpy *= outfit.health_mpy
        total_strength_add += outfit.strength_add
        total_strength_mpy *= outfit.strength_mpy
        total_agility_add += outfit.agility_add
        total_agility_mpy *= outfit.agility_mpy
    else:
        outfit_name = "нет"
    meal_id_list = await effect_commands.select_user_current_meals(user.user_id)
    for meal_id in meal_id_list:
        cur_meal = await meal_commands.select_meal(meal_id)
        total_strength_add += cur_meal.strength_add
        total_agility_add += cur_meal.agility_add
        total_strength_mpy *= cur_meal.strength_mpy
        total_agility_mpy *= cur_meal.agility_mpy
    total_max_health = user.max_health * total_max_health_mpy + total_max_health_add
    total_strength = user.strength * total_strength_mpy + total_strength_add
    total_agility = user.agility * total_agility_mpy + total_agility_add
    status = (f"Информация о шибе игрока {sender_link}:"
              f"\n\U0001F415 Имя шибы: {user.shiba_name}"
              f"\n\U0001F31F Уровень шибы: {user.level}"
              f"\n\U00002728 Очков опыта: {user.exp}"
              f"\n\U00002B06 Очков улучшений: {user.level_up}"
              f"\n\U00002764 Здоровье шибы: {user.health}/{int(total_max_health)}"
              f"\n\U0001F4AA Сила шибы: {int(total_strength)}"
              f"\n\U0001F977 Ловкость шибы: {int(total_agility)}"
              f"\n\U0001F4B4 Денег: {user.money}"
              f"\n\U0001F5E1 Экипированное оружие: {weapon_name}"
              f"\n\U0001F458 Экипированная одежда: {outfit_name}")
    if user.pic_path is not None:
        await dp.bot.send_photo(
            message.chat.id,
            InputFile(path_or_bytesio=pathlib.Path(__file__).parent / "../../user_pictures/used/" / user.pic_path),
            caption=status,
            reply_markup=await get_my_shiba_menu(user_id=message.from_user.id)
        )
    else:
        await message.answer(
            status,
            reply_markup=await get_my_shiba_menu(user_id=message.from_user.id),
            disable_web_page_preview=True
        )
