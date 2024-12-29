from .else_action import *
from .round_action import *
from .Info import *
from .props import *


async def shoot_to_self(uid,uid2):
    """
    射击自己
    """
    ad = 1
    if await get_knife_type(uid):
        ad += 1
    if await check_first_act(uid):
        if await check_bullet_type(uid) == "空弹":
            await after_shoot(uid)
            return True, {'thebullet': '空弹', 'first_change' : uid , "hurt" : 0 ,'user' : [uid, uid2]}
        else:
            if await get_blood(uid) > ad:
                if await get_handcuffs_type(uid):
                    await after_shoot(uid)
                    await delet_blood(uid, ad)
                    return True, {'thebullet': '实弹', 'first_change' : uid, "hurt":ad, 'user' : [uid, uid2]}
                else:
                    await after_shoot(uid)
                    await delet_blood(uid, ad)
                    await change_first_act(uid)
                    return True, {'thebullet': '实弹', 'first_change' : uid2, "hurt":ad, 'user' : [uid, uid2]}
            else:
                type,res = await change_round(uid, uid2)
                res.update({'thebullet': '实弹', 'first_change' : uid, "hurt":ad, 'user' : [uid, uid2]})
                return True,res
    else:
        return False, {'type': False , 'msg': '不是该用户的回合', 'user' : [uid, uid2]}



async def shoot_to_opponent(uid, uid2):
    """
    射击对手
    """
    ad = 1
    if await get_knife_type(uid):
        ad += 1
    if await check_first_act(uid):
        if await check_bullet_type(uid) == "空弹":
            if await get_handcuffs_type(uid):
                await after_shoot(uid)
                return True, {'thebullet': '空弹', 'first_change' : uid , "hurt" : 0, 'user' : [uid, uid2]}
            else:
                await change_first_act(uid)
                await after_shoot(uid)
                return True, {'thebullet': '空弹', 'first_change' : uid2 , "hurt" : 0, 'user' : [uid, uid2]}
        else:
            if await get_blood(uid2) > ad:
                if await get_handcuffs_type(uid):
                    await after_shoot(uid)
                    await delet_blood(uid2, ad)
                    return True, {'thebullet': '实弹', 'first_change' : uid, "hurt":ad, 'user' : [uid, uid2]}
                else:
                    await after_shoot(uid)
                    await delet_blood(uid2, ad)
                    await change_first_act(uid)
                    return True, {'thebullet': '实弹', 'first_change' : uid2, "hurt":ad, 'user' : [uid, uid2]}
            else:
                type,res = await change_round(uid, uid2)
                if type:
                    pass
                else:
                    await change_first_act(uid)
                res.update({'thebullet': '实弹', 'first_change' : uid2, "hurt":ad})
                return True, res
    else:
        return False, {'type': False , 'msg': '不是该用户的回合', 'user' : [uid, uid2]}



async def shoot_action(uid, target):
    """
    射击操作
    """
    uid2 = await get_opponent(uid)
    num = await check_bullet_num(uid)
    if num != False:
        if num > 1:
            if target == "self":
                type,data = await shoot_to_self(uid, uid2)
            elif target == "opponent":
                type,data = await shoot_to_opponent(uid, uid2)
        else:
            if target == "self":
                type,data = await shoot_to_self(uid, uid2)
            elif target == "opponent":
                type,data = await shoot_to_opponent(uid, uid2)
            if type:
                data1 = await add_bullet_props(uid, uid2)
                data.update(data1)
            else:
                pass
    else:
        data = {'type':False,'msg':'子弹不足', 'user' : [uid, uid2]}
    blood1 = await get_blood(uid)
    blood2 = await get_blood(uid2)
    blood = {'blood':{f'{uid}':blood1,f'{uid2}':blood2}}
    data.update(blood)
    return data
async def use_prop(uid,target):
    """
    使用道具(非偷偷)
    """
    props_action_list = {
        '小刀':use_prop_xiaodao,
        '华子':use_prop_huazi,
        '饮料':use_prop_yingliao,
        '手机':use_prop_shouji,
        '骰子':use_prop_touzi,
        '手铐':use_prop_shoukao,
        '过期药':use_prop_guoqiyao,
        '放大镜':use_prop_fangdajing,
        '逆转器':use_prop_nizhuanqi,
        'xiaodao': use_prop_huazi,
        'huazi': use_prop_huazi,
        'shouji': use_prop_shouji,
        'touzi': use_prop_touzi,
        'yingliao': use_prop_yingliao,
        'shoukao': use_prop_shoukao,
        'guoqiyao': use_prop_guoqiyao,
        'fangdajing': use_prop_fangdajing,
        'nizhuanqi': use_prop_nizhuanqi
    }
    uid2 = await get_opponent(uid)
    if target not in props_action_list.keys():
        return {'type':False,'msg':'道具不存在', 'user' : [uid, uid2]}
    if await check_first_act(uid):
        type,data = await props_action_list[target](uid,False)
        if type:
            blood1 = await get_blood(uid)
            blood2 = await get_blood(uid2)
            blood = {'blood':{f'{uid}':blood1,f'{uid2}':blood2}, 'user' : [uid, uid2]}
            data.update(blood)
        else:
            user_list = {'user': [uid, uid2]}
            data.update(user_list)
    else:
        data = {'type':False,'msg':'不是该用户的回合', 'user' : [uid, uid2]}
    return data


async def use_steal_prop(uid,target):
    """
    使用道具(偷偷)
    """
    props_action_list = {
        '小刀':use_prop_xiaodao,
        '华子':use_prop_huazi,
        '饮料':use_prop_yingliao,
        '手机':use_prop_shouji,
        '骰子':use_prop_touzi,
        '手铐':use_prop_shoukao,
        '过期药':use_prop_guoqiyao,
        '放大镜':use_prop_fangdajing,
        '逆转器':use_prop_nizhuanqi,
        'xiaodao': use_prop_huazi,
        'huazi': use_prop_huazi,
        'shouji': use_prop_shouji,
        'touzi': use_prop_touzi,
        'yingliao': use_prop_yingliao,
        'shoukao': use_prop_shoukao,
        'guoqiyao': use_prop_guoqiyao,
        'fangdajing': use_prop_fangdajing,
        'nizhuanqi': use_prop_nizhuanqi
    }
    uid2 = await get_opponent(uid)
    if target not in props_action_list.keys():
        return {'type':False,'msg':'道具不存在', 'user' : [uid, uid2]}
    if await check_first_act(uid):
        type,data = await props_action_list[target](uid,True)
        if type:
            await use_prop_toutou(uid)
            blood1 = await get_blood(uid)
            blood2 = await get_blood(uid2)
            blood = {'blood':{f'{uid}':blood1,f'{uid2}':blood2}, 'user' : [uid, uid2]}
            data.update(blood)
        else:
            user_list = {'user': [uid, uid2]}
            data.update(user_list)
    else:
        data = {'type':False,'msg':'不是该用户的回合', 'user' : [uid, uid2]}
    return data