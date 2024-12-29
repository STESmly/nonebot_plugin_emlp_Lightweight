from .user_info import *
from .emlp_rule import *


Initialize1 = {
    "blood" : 0,   ##血量
    "round" : 1,   ##回合数
    "bullet" : [],  ##子弹
    "props" : [],   ##道具
    "heal" : True,   ##是否可以治疗
    "handcuffs" : False,   ##是否使用手铐
    "first_act" : True,   ##是否是先手
    "knife" : False,   ##是否使用小刀
}

Initialize2 = {
    "status": "空闲",
    "opponent": None
}
async def check_bullet_type(uid,num = 0):
    '''
    检查子弹类型
    '''
    data_path = f'{module_path}/data/game/{uid}.json'
    data = json.load(open(data_path, 'r', encoding='utf-8'))
    return data['bullet'][num]

async def check_bullet_num(uid):
    '''
    检查子弹数量
    '''
    data_path = f'{module_path}/data/game/{uid}.json'
    data = json.load(open(data_path, 'r', encoding='utf-8'))
    num = len(data['bullet'])
    if num == 0:
        return False
    else:
        return num
    
async def change_first_act(uid):
    '''
    改变先手
    '''
    uid1 = uid
    uid2 = await get_opponent(uid1)
    data_path1 = f'{module_path}/data/game/{uid1}.json'
    data_path2 = f'{module_path}/data/game/{uid2}.json'
    data1 = json.load(open(data_path1, 'r', encoding='utf-8'))
    data2 = json.load(open(data_path2, 'r', encoding='utf-8'))
    data1['first_act'] = False
    data2['first_act'] = True
    json.dump(data1, open(data_path1, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
    json.dump(data2, open(data_path2, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

async def check_props(uid,target):
    '''
    检查道具是否存在
    '''
    data_path = f'{module_path}/data/game/{uid}.json'
    data = json.load(open(data_path, 'r', encoding='utf-8'))
    if target in data['props']:
        return True
    else:
        return False

async def after_shoot(uid):
    '''
    消除子弹
    '''
    uid1 = uid
    uid2 = await get_opponent(uid1)
    data_path1 = f'{module_path}/data/game/{uid1}.json'
    data_path2 = f'{module_path}/data/game/{uid2}.json'
    data1 = json.load(open(data_path1, 'r', encoding='utf-8'))
    data2 = json.load(open(data_path2, 'r', encoding='utf-8'))
    data1['bullet'].pop(0)
    data1['handcuffs'] = False
    data1['knife'] = False
    data2['bullet'].pop(0)
    data2['handcuffs'] = False
    data2['knife'] = False
    json.dump(data1, open(data_path1, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
    json.dump(data2, open(data_path2, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

async def delet_blood(uid, ad):
    """
    扣血
    """
    data_path = f'{module_path}/data/game/{uid}.json'
    data = json.load(open(data_path, 'r', encoding='utf-8'))
    data['blood'] -= ad
    if data['blood'] == 1 and data['round'] == 3:
        data['heal'] = False
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

async def add_bullet_props(uid,uid2):
    '''
    补充子弹和道具
    '''
    uid1 = uid
    data_path1 = f'{module_path}/data/game/{uid1}.json'
    data_path2 = f'{module_path}/data/game/{uid2}.json'
    data1 = json.load(open(data_path1, 'r', encoding='utf-8'))
    data2 = json.load(open(data_path2, 'r', encoding='utf-8'))
    bullet = await get_bullet()
    props1, props2 = await props_at(4)
    data1['bullet'] = bullet
    data2['bullet'] = bullet
    data1['props'].extend(props1)
    data2['props'].extend(props2)
    data1['props'] = data1['props'][:8]
    data2['props'] = data2['props'][:8]
    new_props1 = data1['props']
    new_props2 = data2['props']
    res = {
        'user' : [uid1,uid2],
        'props' : {
            f'{uid1}' : new_props1,
            f'{uid2}' : new_props2
        },
        'bullet' : {
            '实弹': bullet.count('实弹'),
            '空弹': bullet.count('空弹')
        },
        'round': data1['round'],
        'status_up' : True
    }
    json.dump(data1, open(data_path1, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
    json.dump(data2, open(data_path2, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
    return res

async def set_bullet_list(uid1, uid2, bullet_list):
    """
    设置子弹列表
    """
    data_path1 = f'{module_path}/data/game/{uid1}.json'
    data_path2 = f'{module_path}/data/game/{uid2}.json'
    data1 = json.load(open(data_path1, 'r', encoding='utf-8'))
    data2 = json.load(open(data_path2, 'r', encoding='utf-8'))
    data1['bullet'] = bullet_list
    data2['bullet'] = bullet_list
    json.dump(data1, open(data_path1, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
    json.dump(data2, open(data_path2, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

async def set_handcuffs_type(uid, handcuffs_type):
    '''
    设置手铐的使用状态(该函数暂时不做调用)
    '''
    data_path = f'{module_path}/data/game/{uid}.json'
    data = json.load(open(data_path, 'r', encoding='utf-8'))
    data['handcuffs'] = handcuffs_type
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)