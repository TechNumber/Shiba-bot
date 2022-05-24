import random

from asyncpg import UniqueViolationError

from utils.db_api import effect_commands
from utils.db_api.db_gino import db
from utils.db_api.meal_commands import select_meal
from utils.db_api.outfit_commands import select_outfit
from utils.db_api.schemas.user import User
from utils.db_api.weapon_commands import select_weapon


async def add_user(user_id: int,
                   user_name: str,
                   shiba_name: str = None,
                   pic_url: str = None,
                   weapon_id: int = None,
                   outfit_id: int = None):
    try:
        user = User(
            user_id=user_id,
            user_name=user_name,
            shiba_name=shiba_name,
            pic_url=pic_url,
            weapon_id=weapon_id,
            outfit_id=outfit_id
        )
        await user.create()

    except UniqueViolationError:
        pass


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def select_user(user_id: int):
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user


async def count_users():
    total = await db.func.count(User.user_id).gino.scalar()
    return total


async def update_shiba_name(user_id, shiba_name):
    user = await User.get(user_id)
    await user.update(shiba_name=shiba_name).apply()


async def update_user_money(user_id, money):
    user = await User.get(user_id)
    await user.update(money=money).apply()


async def update_user_weapon(user_id, weapon_id):
    user = await User.get(user_id)
    await user.update(weapon_id=weapon_id).apply()


async def update_user_outfit(user_id, outfit_id):
    user = await User.get(user_id)
    await user.update(outfit_id=outfit_id).apply()


async def set_weapon_null(user_id):
    user = await User.get(user_id)
    await user.update(weapon_id=None).apply()


async def set_outfit_null(user_id):
    user = await User.get(user_id)
    await user.update(outfit_id=None).apply()


async def get_all_users_id():
    user_id_list = await User.query.gino.load(User.user_id).all()
    return user_id_list





async def calculate_buffs(user_id: int):
    buffs = [0, 0, 1, 1]  # с 0 по 1 - прибавки к силе и ловкости; с 2 по 3 - множители силы и ловкости
    meal_id_list = await effect_commands.select_user_current_meals(user_id)
    for meal_id in meal_id_list:
        cur_meal = await select_meal(meal_id)
        buffs[0] += cur_meal.strength_add
        buffs[1] += cur_meal.agility_add
        buffs[2] *= cur_meal.strength_mpy
        buffs[3] *= cur_meal.agility_mpy
    user = await select_user(user_id)
    weapon = await select_weapon(user.weapon_id)
    buffs[1] += weapon.agility_add
    buffs[3] *= weapon.agility_mpy
    outfit = await select_outfit(user.outfit_id)
    buffs[0] += outfit.strength_add
    buffs[1] += outfit.agility_add
    buffs[2] *= outfit.strength_mpy
    buffs[3] *= outfit.agility_mpy
    return buffs


async def combat_sequence(id1, id2):
    user1 = await select_user(id1)
    user2 = await select_user(id2)
    buffs1 = await calculate_buffs(id1)
    buffs2 = await calculate_buffs(id2)
    weapon1 = await select_weapon(user1.weapon_id)
    weapon2 = await select_weapon(user2.weapon_id)
    u1_name = user1.shiba_name
    u2_name = user2.shiba_name
    u1_str = user1.strength * buffs1[2] + buffs1[0]
    u1_ag = user1.agility * buffs1[3] + buffs1[1]
    u2_str = user2.strength * buffs2[2] + buffs2[0]
    u2_ag = user2.agility * buffs2[3] + buffs2[1]
    u1_dmg = weapon1.damage * (1 + u1_str * 0.1)
    u2_dmg = weapon2.damage * (1 + u2_str * 0.1)
    u1_dodge_rate = u1_ag * 0.02 - u2_ag * 0.005
    u2_dodge_rate = u2_ag * 0.02 - u1_ag * 0.005
    u1_start_hp = user1.health
    u2_start_hp = user1.health
    u1_cur_hp = u1_start_hp
    u2_cur_hp = u2_start_hp
    victor_id = -1
    log = "Дуэль!\n"
    action_captions_strike = [" наносит удар.",
                              " целится в слабое место!",
                              " совершает стремительный выпад.",
                              " несется на противника!", ]
    action_captions_dodge = [" изящно уходит от атаки.",
                             " уклоняется!",
                             " искусно парирует атаку.",
                             " совершает рывок в сторону, избегая атаки."]
    action_captions_hurt = [" получает ранение. Получено урона: ",
                            " не смог увернуться. Получено урона: ",
                            " ощутил вкус клинка. Получено урона: ",
                            " ранен! Получено урона: "]

    for i in range(10):
        caption = u1_name + action_captions_strike[random.randint(0, 3)]
        hit_or_miss = (random.randint(0, 1) <= u2_dodge_rate)
        if hit_or_miss:
            caption += " " + u2_name + action_captions_dodge[random.randint(0, 3)] + "\n"
        else:
            dmg = u1_dmg + random.randint(-10, 10)
            caption += " " + u2_name + action_captions_hurt[random.randint(0, 3)] + str(int(dmg)) + "\n"
            u2_cur_hp -= dmg
        if u2_cur_hp <= 0:
            caption += u1_name + " победил!\n"
            log += caption
            victor_id = id1
            break
        caption += u2_name + action_captions_strike[random.randint(0, 3)]
        hit_or_miss = (random.randint(0, 1) <= u1_dodge_rate)
        if hit_or_miss:
            caption += " " + u1_name + action_captions_dodge[random.randint(0, 3)] + "\n"
        else:
            dmg = u2_dmg + random.randint(-10, 10)
            caption += " " + u1_name + action_captions_hurt[random.randint(0, 3)] + str(int(dmg)) + "\n"
            u1_cur_hp -= dmg
        if u1_cur_hp <= 0:
            caption += u2_name + " победил!\n"
            log += caption
            victor_id = id2
            break
        log += caption
        log += "<>\n"
    if victor_id is None:
        u1_dmg_dealt = u2_cur_hp / u2_start_hp
        u2_dmg_dealt = u1_cur_hp / u1_start_hp
        if u1_dmg_dealt > u2_dmg_dealt:
            victor_id = id1
            log += u1_name + " победил!\n"
        elif u2_dmg_dealt > u1_dmg_dealt:
            victor_id = id2
            log += u2_name + " победил!\n"
        else:
            victor_id = -1
            log += "Ничья!\n"
    if victor_id == id1:
        cur_exp1 = user1.exp + 50 + random.randint(-15, 25)
        await user1.update(exp=cur_exp1).apply()
    elif victor_id == id2:
        cur_exp2 = user2.exp + 50 + random.randint(-15, 25)
        await user2.update(exp=cur_exp2).apply()
    else:
        cur_exp1 = (user1.exp + 50 + random.randint(-15, 25)) // 2
        cur_exp2 = (user2.exp + 50 + random.randint(-15, 25)) // 2
        await user1.update(exp=cur_exp1).apply()
        await user2.update(exp=cur_exp2).apply()
    await user1.update(health=u1_cur_hp).apply()
    await user2.update(health=u2_cur_hp).apply()
    return log


async def check_level_up(user_id: int):
    lvlup_points = 0
    user = await select_user(user_id)
    cur_lvl = user.level
    max_exp = cur_lvl * 25
    cur_exp = user.exp
    while cur_exp > max_exp:
        lvlup_points += 1
        cur_lvl += 1
        cur_exp -= max_exp
        max_exp = cur_lvl * 25
    await user.update(level=cur_lvl).apply()
    await user.update(exp=cur_exp).apply()
    return lvlup_points


async def check_knockout(user_id):
    ko_status = False
    user = await select_user(user_id)
    cur_hp = user.health
    if cur_hp <= 0:
        ko_status = True
        await user.update(exp=0).apply()
    return ko_status
