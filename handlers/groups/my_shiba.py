import pathlib

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import InputFile

from keyboards.inline.my_shiba.my_shiba_menus import get_my_shiba_menu
from loader import dp
from states.game_state import GameState
from utils.db_api import user_commands, weapon_commands, outfit_commands


@dp.message_handler(Command("my_shiba"), state=GameState.registered)
async def show_my_shiba_menu(message: types.Message):
    if message.from_user.username is not None:
        sender_link = f"<a href=\"t.me/{message.from_user.username}\">{message.from_user.username}</a>"
    else:
        sender_link = f"<a href=\"tg://user?id={message.from_user.id}\">{message.from_user.full_name}</a>"
    user = await user_commands.select_user(message.from_user.id)
    equipped_weapon = (
        await weapon_commands.select_weapon(user.weapon_id)
    ).weapon_name if user.weapon_id is not None else 'нет'
    equipped_outfit = (
        await outfit_commands.select_outfit(user.outfit_id)
    ).outfit_name if user.outfit_id is not None else 'нет'
    if user.pic_path is not None:
        await dp.bot.send_photo(
            message.chat.id,
            InputFile(path_or_bytesio=pathlib.Path(__file__).parent / "../../user_pictures/used/" / user.pic_path),
            f"Информация о шибе игрока {sender_link}:"
            f"\n\U0001F415 Имя шибы: {user.shiba_name}"
            f"\n\U0001F31F Уровень шибы: {user.level}"
            f"\n\U00002728 Очков опыта: {user.exp}"
            f"\n\U00002B06 Очков улучшений: {user.level_up}"
            f"\n\U00002764 Здоровье шибы: {user.health}/{user.max_health}"
            f"\n\U0001F4AA Сила шибы: {user.strength}"
            f"\n\U0001F977 Ловкость шибы: {user.agility}"
            f"\n\U0001F4B4 Денег: {user.money}",
            f"\n\U0001F5E1 Экипированное оружие: {equipped_weapon}"
            f"\n\U0001F458 Экипированная одежда: {equipped_outfit}",
            reply_markup=await get_my_shiba_menu(user_id=message.from_user.id)
        )
    else:
        await message.answer(
            f"Информация о шибе игрока {sender_link}:"
            f"\n\U0001F415 Имя шибы: {user.shiba_name}"
            f"\n\U0001F31F Уровень шибы: {user.level}"
            f"\n\U00002728 Очков опыта: {user.exp}"
            f"\n\U00002B06 Очков улучшений: {user.level_up}"
            f"\n\U00002764 Здоровье шибы: {user.health}/{user.max_health}"
            f"\n\U0001F4AA Сила шибы: {user.strength}"
            f"\n\U0001F977 Ловкость шибы: {user.agility}"
            f"\n\U0001F4B4 Денег: {user.money}"
            f"\n\U0001F5E1 Экипированное оружие: {equipped_weapon}"
            f"\n\U0001F458 Экипированная одежда: {equipped_outfit}",
            reply_markup=await get_my_shiba_menu(user_id=message.from_user.id),
            disable_web_page_preview=True
        )

        # TODO: просмотр того, что экипировано в данный момент
