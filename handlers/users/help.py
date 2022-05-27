from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from filters.is_chat import IsChat
from loader import dp


@dp.message_handler(CommandHelp(), IsChat())
async def bot_help(message: types.Message):
    if message.from_user.username is not None:
        sender_link = f"<a href=\"t.me/{message.from_user.username}\">{message.from_user.username}</a>"
    else:
        sender_link = f"<a href=\"tg://user?id={message.from_user.id}\">{message.from_user.full_name}</a>"
    await dp.bot.send_message(
        message.from_user.id,
        f"Приветствую, {sender_link}!\n\n"
        f"Здесь ты можешь ознакомиться с правилами игры\n\n"
        f"В ходе игры ты сможешь сражаться с монстрами из подземелий (команда /mob_fight ) или другими игроками ("
        f"\nкоманда /duel @имя_игрока ). "
        f"За ход боя отвечают три характеристики: <b>здоровье</b>, <b>сила</b> и <b>ловкость</b>.\n"
        f"Победителем считается тот, кто смог нанести больше урона противнику. "
        f"Победитель получает очки <b>опыта</b> (а за уничтожение монстра — ещё и <b>деньги</b>). "
        f"По накоплении определённого количества <b>опыта</b> шиба переходит на следующий <b>уровень</b>. С повышением уровня собака "
        f"получает <b>очки улучшений</b>, которые можно потратить на повышение одной из трёх вышеупомянутых базовых "
        f"характеристик.\n\nЗа что отвечают базовые характеристики? \n"
        f"<b>Здоровье</b> определяет, вынесет ли твоя шиба сокрушительную серию ударов врага. Если уровень здоровья по итогу "
        f"сражения упадёт до нуля, твоя собака погибнет. Но не волнуйся, на острове поселилась известная группа "
        f"монахов с Хоккайдо, освоивших искусство реинкарнации. Твоя шиба будет возрождена и сможет продолжить "
        f"свой путь, однако весь опыт, накопленный ею с момента последнего повышения уровня, будет потерян.\n\n"
        f"<b>Сила</b> отвечает за наносимый шибой урон. Чем больше урона наносит шиба, тем больше здоровья модет потерять "
        f"противник, и тем ближе твой пёс к победе.\n\n"
        f"<b>Ловкость</b> определяет шанс уклонения шибы от удара. При этом решающую роль в успешности уклонения играет не "
        f"сам уровень показателя ловкости, а разница в значениях этого показателя у дуэлянтов: чем выше ловкость "
        f"вашего пса в сравнении с ловкостью противника, тем выше шанс уклонения.\n\n"
        f"Безусловно, сражаться голыми руками не очень эффективно. Накопленные за истребление монстров деньги можно "
        f"потратить в <b>магазине</b> (команда /shop ). В магазине продаются <b>оружие</b>, <b>одежда</b> и <b>еда</b>. Обычно оружие увеличивает "
        f"наносимый урон, одежда — здоровье в бою и ловкость, а еда позволяет исцелиться. Подробнее об этих и других эффектах оружия, одежды и еды "
        f"можно почитать в их описании в магазине.\n\n"
        f"Купленные предметы хранятся в <b>инвентаре</b> шибы (команда /inventory ). Там же их можно экипировать или "
        f"выбросить.\n\n"
        f"Чтобы узнать текущую информацию о своей шибе, отправь команду /my_shiba . Из меню шибы можно также перейти "
        f"в магазин или инвентарь, отправиться на сражение с монстром или сменить имя шибы. \n\n"
        f"Удачной игры!",
        disable_web_page_preview=True
    )
