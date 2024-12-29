from .else_action import *
from .user_info import *
from .round_action import *


"""
小刀
华子
饮料
手机
骰子
手铐
偷偷
过期药
放大镜
逆转器
"""

async def use_prop_xiaodao(uid,toutou_type):
    """
    使用道具小刀
    """
    uid2 = await get_opponent(uid)
    if not toutou_type:
        if await check_props(uid, '小刀'):
            knife_type = await get_knife_type(uid)
            if knife_type:
                return False , {'type':False,'msg':'该道具无法重复使用'}
            else:
                data_path = f'{module_path}/data/game/{uid}.json'
                data = json.load(open(data_path, 'r', encoding='utf-8'))
                data['knife'] = True
                data['props'].remove('小刀')
                json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
                return True, {'type':True,'msg':'使用成功'}
        else:
            return False, {'type':False,'msg':'道具不存在'}
    elif toutou_type:
        if await check_props(uid2, '小刀'):
            knife_type = await get_knife_type(uid)
            if knife_type:
                return False , {'type':False,'msg':'该道具无法重复使用'}
            else:
                data_path1 = f'{module_path}/data/game/{uid}.json'
                data_path2 = f'{module_path}/data/game/{uid2}.json'
                data1 = json.load(open(data_path1, 'r', encoding='utf-8'))
                data2 = json.load(open(data_path2, 'r', encoding='utf-8'))
                data1['knife'] = True
                data2['props'].remove('小刀')
                json.dump(data1, open(data_path1, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
                json.dump(data2, open(data_path2, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
                return True, {'type':True,'msg':'使用成功'}
        else:
            return False, {'type':False,'msg':'道具不存在'}
    
async def use_prop_huazi(uid,toutou_type):
    """
    使用道具华子
    """
    uid2 = await get_opponent(uid)
    if not toutou_type:
        if await check_props(uid, '华子'):    
            heal_type = await get_heal_type(uid)
            blood = await get_blood(uid)
            if heal_type:
                data_path = f'{module_path}/data/game/{uid}.json'
                data = json.load(open(data_path, 'r', encoding='utf-8'))
                data['blood'] = blood + 1
                data['props'].remove('华子')
                json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
                return True, {'type':True,'msg':'使用成功','hurt': 1}
            else:
                return False , {'type':False,'msg':'该状态无法回血'}
        else:
            return False, {'type':False,'msg':'道具不存在'}
    elif toutou_type:
        if await check_props(uid2, '华子'):    
            heal_type = await get_heal_type(uid)
            blood = await get_blood(uid)
            if heal_type:
                data_path1 = f'{module_path}/data/game/{uid}.json'
                data_path2 = f'{module_path}/data/game/{uid2}.json'
                data1 = json.load(open(data_path1, 'r', encoding='utf-8'))
                data2 = json.load(open(data_path2, 'r', encoding='utf-8'))
                data1['blood'] = blood + 1
                data2['props'].remove('华子')
                json.dump(data1, open(data_path1, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
                json.dump(data2, open(data_path2, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
                return True, {'type':True,'msg':'使用成功','hurt': 1}
            else:
                return False , {'type':False,'msg':'该状态无法回血'}
        else:
            return False, {'type':False,'msg':'道具不存在'}
    
async def use_prop_yingliao(uid,toutou_type):
    """
    使用道具饮料
    """
    uid2 = await get_opponent(uid)
    if not toutou_type:
        if await check_props(uid, '饮料'):
            num = await check_bullet_num(uid)
            if num >1:
                bullet = await check_bullet_type(uid)
                await after_shoot(uid)
                data = {
                    'type':True,
                    'msg':f'使用成功,退掉了{bullet}',
                    'thebullet' : bullet
                }
            else:
                bullet = await check_bullet_type(uid)
                await after_shoot(uid)
                data = {
                    'type':True,
                    'msg':f'使用成功,退掉了{bullet}',
                    'thebullet' : bullet
                }
                data1 = await add_bullet_props(uid, uid2)
                data.update(data1)
            data_path = f'{module_path}/data/game/{uid}.json'
            res = json.load(open(data_path, 'r', encoding='utf-8'))
            res['props'].remove('饮料')
            json.dump(res, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
            return True,data
        else:
            return False, {'type':False,'msg':'道具不存在'}
    elif toutou_type:
        if await check_props(uid2, '饮料'):
            num = await check_bullet_num(uid)
            if num >1:
                bullet = await check_bullet_type(uid)
                await after_shoot(uid)
                data = {
                    'type':True,
                    'msg':f'使用成功,退掉了{bullet}',
                    'thebullet' : bullet
                }
            else:
                bullet = await check_bullet_type(uid)
                await after_shoot(uid)
                data = {
                    'type':True,
                    'msg':f'使用成功,退掉了{bullet}',
                    'thebullet' : bullet
                }
                data1 = await add_bullet_props(uid, uid2)
                data.update(data1)
            data_path = f'{module_path}/data/game/{uid2}.json'
            res = json.load(open(data_path, 'r', encoding='utf-8'))
            res['props'].remove('饮料')
            json.dump(res, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
            return True,data
        else:
            return False, {'type':False,'msg':'道具不存在'}
    
async def use_prop_shouji(uid,toutou_type):
    """
    使用道具手机
    """
    uid2 = await get_opponent(uid)
    if not toutou_type:
        if await check_props(uid, '手机'):
            num = await check_bullet_num(uid)
            num = random.randint(0,num-1)
            bullet = await check_bullet_type(uid,num)
            data = {
                'type':True,
                'msg':f'使用成功,第{num+1}颗子弹是{bullet}',
                'thebullet' : bullet,
                'use_phone':num+1,
                'private_type':True
            }
            data_path = f'{module_path}/data/game/{uid}.json'
            res = json.load(open(data_path, 'r', encoding='utf-8'))
            res['props'].remove('手机')
            json.dump(res, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
            return True,data
        else:
            return False, {'type':False,'msg':'道具不存在'}
    elif toutou_type:
        if await check_props(uid2, '手机'):
            num = await check_bullet_num(uid)
            num = random.randint(0,num-1)
            bullet = await check_bullet_type(uid,num)
            data = {
                'type':True,
                'msg':f'使用成功,第{num+1}颗子弹是{bullet}',
                'thebullet' : bullet,
                'use_phone':num+1,
                'private_type':True
            }
            data_path = f'{module_path}/data/game/{uid2}.json'
            res = json.load(open(data_path, 'r', encoding='utf-8'))
            res['props'].remove('手机')
            json.dump(res, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
            return True,data
        else:
            return False, {'type':False,'msg':'道具不存在'}
async def use_prop_touzi(uid, toutou_type):
    """
    使用道具骰子
    """
    uid2 = await get_opponent(uid)
    if not toutou_type:
        if await check_props(uid, '骰子'):
            bullet = await get_bullet_list(uid)
            random.shuffle(bullet)
            await set_bullet_list(uid,uid2,bullet)
            data = {
                'type':True,
                'msg':'使用成功,子弹顺序已打乱'
            }
            data_path = f'{module_path}/data/game/{uid}.json'
            res = json.load(open(data_path, 'r', encoding='utf-8'))
            res['props'].remove('骰子')
            json.dump(res, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
            return True,data
        else:
            return False, {'type':False,'msg':'道具不存在'}
    elif toutou_type:
        if await check_props(uid2, '骰子'):
            bullet = await get_bullet_list(uid)
            random.shuffle(bullet)
            await set_bullet_list(uid,uid2,bullet)
            data = {
                'type':True,
                'msg':'使用成功,子弹顺序已打乱'
            }
            data_path = f'{module_path}/data/game/{uid2}.json'
            res = json.load(open(data_path, 'r', encoding='utf-8'))
            res['props'].remove('骰子')
            json.dump(res, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
            return True,data
        else:
            return False, {'type':False,'msg':'道具不存在'}

async def use_prop_shoukao(uid,toutou_type):
    """
    使用道具手铐
    """
    uid2 = await get_opponent(uid)
    if not toutou_type:
        if await check_props(uid, '手铐'):
            handcuffs_type = await get_handcuffs_type(uid)
            if handcuffs_type:
                return False , {'type':False,'msg':'该道具无法重复使用'}
            else:
                data_path = f'{module_path}/data/game/{uid}.json'
                data = json.load(open(data_path, 'r', encoding='utf-8'))
                data['handcuffs'] = True
                data['props'].remove('手铐')
                json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
                return True, {'type':True,'msg':'使用成功'}
        else:
            return False, {'type':False,'msg':'道具不存在'}
    elif toutou_type:
        if await check_props(uid2, '手铐'):
            handcuffs_type = await get_handcuffs_type(uid)
            if handcuffs_type:
                return False , {'type':False,'msg':'该道具无法重复使用'}
            else:
                data_path1 = f'{module_path}/data/game/{uid}.json'
                data_path2 = f'{module_path}/data/game/{uid2}.json'
                data1 = json.load(open(data_path1, 'r', encoding='utf-8'))
                data2 = json.load(open(data_path2, 'r', encoding='utf-8'))
                data1['handcuffs'] = True
                data2['props'].remove('手铐')
                json.dump(data1, open(data_path1, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
                json.dump(data2, open(data_path2, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
                return True, {'type':True,'msg':'使用成功'}
        else:
            return False, {'type':False,'msg':'道具不存在'}

async def use_prop_guoqiyao(uid,toutou_type):
    """
    使用道具过期药
    """
    uid2 = await get_opponent(uid)
    if not toutou_type:
        if await check_props(uid, '过期药'):    
            heal_type = await get_heal_type(uid)
            blood = await get_blood(uid)
            use_type = random.choices([True,False],k=1)[0]
            if heal_type and use_type:
                data_path = f'{module_path}/data/game/{uid}.json'
                data = json.load(open(data_path, 'r', encoding='utf-8'))
                data['blood'] = blood + 2
                data['props'].remove('过期药')
                json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
                return True, {'type':True,'msg':'使用成功','hurt': 2}
            elif heal_type and not use_type:
                if blood > 1:
                    data_path = f'{module_path}/data/game/{uid}.json'
                    data = json.load(open(data_path, 'r', encoding='utf-8'))
                    data['props'].remove('过期药')
                    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
                    await delet_blood(uid, 1)
                    return True, {'type':True,'msg':'使用成功','hurt': -1}
                else:
                    type,res = await change_round(uid, uid2)
                    res.update({'first_change' : uid, "hurt":-1, 'user' : [uid, uid2]})
                    return True, res
            else:
                return False , {'type':False,'msg':'该状态无法回血'}
        else:
            return False, {'type':False,'msg':'道具不存在'}
    elif toutou_type:
        if await check_props(uid2, '过期药'):    
            heal_type = await get_heal_type(uid)
            blood = await get_blood(uid)
            use_type = random.choices([True,False],k=1)[0]
            if heal_type and use_type:
                data_path1 = f'{module_path}/data/game/{uid}.json'
                data_path2 = f'{module_path}/data/game/{uid2}.json'
                data1 = json.load(open(data_path1, 'r', encoding='utf-8'))
                data2 = json.load(open(data_path2, 'r', encoding='utf-8'))
                data1['blood'] = blood + 2
                data2['props'].remove('过期药')
                json.dump(data1, open(data_path1, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
                json.dump(data2, open(data_path2, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
                return True, {'type':True,'msg':'使用成功','hurt': 2}
            elif heal_type and not use_type:
                if blood > 1:
                    data_path2 = f'{module_path}/data/game/{uid2}.json'
                    data2 = json.load(open(data_path2, 'r', encoding='utf-8'))
                    data2['props'].remove('过期药')
                    json.dump(data2, open(data_path2, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
                    await delet_blood(uid, 1)
                    return True, {'type':True,'msg':'使用成功','hurt': -1}
                else:
                    type,res = await change_round(uid, uid2)
                    res.update({'first_change' : uid, "hurt":-1, 'user' : [uid, uid2]})
                    return True, res
            else:
                return False , {'type':False,'msg':'该状态无法回血'}
        else:
            return False, {'type':False,'msg':'道具不存在'}
async def use_prop_fangdajing(uid,toutou_type):
    """
    使用道具放大镜
    """
    uid2 = await get_opponent(uid)
    if not toutou_type:
        if await check_props(uid, '放大镜'):
            bullet = await check_bullet_type(uid)
            data = {
                'type':True,
                'msg':f'使用成功,当前子弹是{bullet}',
                'thebullet' : bullet
            }
            data_path = f'{module_path}/data/game/{uid}.json'
            res = json.load(open(data_path, 'r', encoding='utf-8'))
            res['props'].remove('放大镜')
            json.dump(res, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
            return True,data
        else:
            return False, {'type':False,'msg':'道具不存在'}
    elif toutou_type:
        if await check_props(uid2, '放大镜'):
            bullet = await check_bullet_type(uid)
            data = {
                'type':True,
                'msg':f'使用成功,当前子弹是{bullet}',
                'thebullet' : bullet
            }
            data_path = f'{module_path}/data/game/{uid2}.json'
            res = json.load(open(data_path, 'r', encoding='utf-8'))
            res['props'].remove('放大镜')
            json.dump(res, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
            return True,data
        else:
            return False, {'type':False,'msg':'道具不存在'}

async def use_prop_nizhuanqi(uid,toutou_type):
    """
    使用道具逆转器
    """
    uid2 = await get_opponent(uid)
    if not toutou_type:
        if await check_props(uid, '逆转器'):
            bullet = await get_bullet_list(uid)
            if bullet[0] == '实弹':
                bullet[0] = '空弹'
            elif bullet[0] == '空弹':
                bullet[0] = '实弹'
            await set_bullet_list(uid,uid2,bullet)
            data = {
                'type':True,
                'msg':'使用成功'
            }
            data_path = f'{module_path}/data/game/{uid}.json'
            res = json.load(open(data_path, 'r', encoding='utf-8'))
            res['props'].remove('逆转器')
            json.dump(res, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
            return True,data
        else:
            return False, {'type':False,'msg':'道具不存在'}
    elif toutou_type:
        if await check_props(uid2, '逆转器'):
            bullet = await get_bullet_list(uid)
            if bullet[0] == '实弹':
                bullet[0] = '空弹'
            elif bullet[0] == '空弹':
                bullet[0] = '实弹'
            await set_bullet_list(uid,uid2,bullet)
            data = {
                'type':True,
                'msg':'使用成功'
            }
            data_path = f'{module_path}/data/game/{uid2}.json'
            res = json.load(open(data_path, 'r', encoding='utf-8'))
            res['props'].remove('逆转器')
            json.dump(res, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
            return True,data
        else:
            return False, {'type':False,'msg':'道具不存在'}

async def use_prop_toutou(uid):
    """
    使用道具偷偷
    """
    if await check_props(uid, '偷偷'):
            data = {
                'type':True,
                'msg':'使用成功'
            }
            data_path = f'{module_path}/data/game/{uid}.json'
            res = json.load(open(data_path, 'r', encoding='utf-8'))
            res['props'].remove('偷偷')
            json.dump(res, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
            return True,data
    else:
        return False, {'type':False,'msg':'道具不存在'}