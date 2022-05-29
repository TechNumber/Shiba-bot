from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Войти в игру"),
            types.BotCommand("help", "Узнать правила игры"),
            types.BotCommand("my_shiba", "Открыть меню персонажа"),
            types.BotCommand("duel", "Вызвать игрока на дуэль"),
            types.BotCommand("mob_fight", "Сразиться с монстром подземелья"),
            types.BotCommand("shop", "Открыть магазин"),
            types.BotCommand("inventory", "Открыть инвентарь"),
            types.BotCommand("level_up", "Открыть меню повышения характеристик"),
            types.BotCommand("shiba_rename", "Переименовать шибу")
        ]
    )
