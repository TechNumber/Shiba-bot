from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from filters import IsCalledByOwner
from keyboards.inline.callback_datas import cancel_callback, level_attribute_up_callback, apply_level_up_callback
from keyboards.inline.level_up.level_up_menus import get_level_up_menu
from loader import dp
from states.game_state import GameState
from utils.db_api import user_commands


@dp.message_handler(Command("level_up"), state=GameState.registered)
async def show_level_up_menu(message: types.Message, state: FSMContext):
    user = await user_commands.select_user(message.from_user.id)
    if user.level_up == 0:
        await message.answer("Похоже, у вас нет очков повышения характеристик... "
                             "Доблестно сражайтесь с другими игроками или с монстрами подземелий, чтобы заработать "
                             "очки повышения характеристик!")
    else:
        level_up_menu = await get_level_up_menu(user,
                                                max_health_added_points=0,
                                                strength_added_points=0,
                                                agility_added_points=0)
        await message.answer(f"У Вас есть {user.level_up} очков повышения характеристик. Вы можете потратить их на "
                             "увеличение показателей здоровья, силы или ловкости. Выбирайте с умом!",
                             reply_markup=level_up_menu)
        await GameState.level_up.set()
        await state.update_data(
            {
                "level_up_points": user.level_up,
                "max_health_added_points": 0,
                "strength_added_points": 0,
                "agility_added_points": 0
            }
        )


@dp.callback_query_handler(IsCalledByOwner(), cancel_callback.filter(cancel_type="level_up"), state=GameState.level_up)
async def cancel_level_up(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await call.answer(cache_time=15)
    await state.reset_data()
    await GameState.registered.set()


@dp.callback_query_handler(IsCalledByOwner(), level_attribute_up_callback.filter(),
                           state=GameState.level_up)
async def level_max_health_up(call: CallbackQuery, state: FSMContext):
    points_distribution = await state.get_data()
    if points_distribution["level_up_points"] > 0:
        attribute_type = (call.data.split(":"))[-1]
        if attribute_type == "max_health":
            await state.update_data(max_health_added_points=points_distribution["max_health_added_points"] + 1)
            points_distribution["max_health_added_points"] += 1
        elif attribute_type == "strength":
            await state.update_data(strength_added_points=points_distribution["strength_added_points"] + 1)
            points_distribution["strength_added_points"] += 1
        elif attribute_type == "agility":
            await state.update_data(agility_added_points=points_distribution["agility_added_points"] + 1)
            points_distribution["agility_added_points"] += 1
        await state.update_data(level_up_points=points_distribution["level_up_points"] - 1)
        points_distribution["level_up_points"] -= 1
        await call.message.edit_text(
            f"У Вас есть {points_distribution['level_up_points']} очков повышения характеристик. "
            "Вы можете потратить их на увеличение показателей здоровья, силы или ловкости. "
            "Выбирайте с умом!")
        user = await user_commands.select_user(user_id=call.from_user.id)
        await call.message.edit_reply_markup(await get_level_up_menu(
            user,
            max_health_added_points=points_distribution["max_health_added_points"],
            strength_added_points=points_distribution["strength_added_points"],
            agility_added_points=points_distribution["agility_added_points"]))


@dp.callback_query_handler(IsCalledByOwner(), apply_level_up_callback.filter(),
                           state=GameState.level_up)
async def level_max_health_up(call: CallbackQuery, state: FSMContext):
    points_distribution = await state.get_data()
    if points_distribution["max_health_added_points"] + \
            points_distribution["strength_added_points"] + \
            points_distribution["agility_added_points"] > 0:
        user = await user_commands.select_user(call.from_user.id)
        await user.update(level_up=points_distribution["level_up_points"],
                          max_health=user.max_health + 10 * points_distribution["max_health_added_points"],
                          strength=user.strength + 1 * points_distribution["strength_added_points"],
                          agility=user.agility + 1 * points_distribution["agility_added_points"]).apply()
        await state.update_data(max_health_added_points=0,
                                strength_added_points=0,
                                agility_added_points=0)
        points_distribution = await state.get_data()
        await call.message.edit_text(
            f"У Вас есть {points_distribution['level_up_points']} очков повышения характеристик. "
            "Вы можете потратить их на увеличение показателей здоровья, силы или ловкости. "
            "Выбирайте с умом!")
        await call.message.edit_reply_markup(await get_level_up_menu(
            user,
            max_health_added_points=points_distribution["max_health_added_points"],
            strength_added_points=points_distribution["strength_added_points"],
            agility_added_points=points_distribution["agility_added_points"]))
