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
    data_path = f'{game_path}/{uid}.json'
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['bullet'][num]

async def check_bullet_num(uid):
    '''
    检查子弹数量
    '''
    data_path = f'{game_path}/{uid}.json'
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    num = len(data['bullet'])
    if num == 0:
        return False
    else:
        return num
    
async def change_first_act(uid1):
    '''
    改变先手
    '''
    uid2 = await get_opponent(uid1)
    data_path1 = f'{game_path}/{uid1}.json'
    data_path2 = f'{game_path}/{uid2}.json'
    with open(data_path1, 'r', encoding='utf-8') as f:
        data1 = json.load(f)
    with open(data_path2, 'r', encoding='utf-8') as f:
        data2 = json.load(f)
    data1['first_act'] = False
    data2['first_act'] = True
    with open(data_path1, 'w', encoding='utf-8') as f:
        json.dump(data1, f, ensure_ascii=False, indent=4)
    with open(data_path2, 'w', encoding='utf-8') as f:
        json.dump(data2, f, ensure_ascii=False, indent=4)

async def check_props(uid,target):
    '''
    检查道具是否存在
    '''
    data_path = f'{game_path}/{uid}.json'
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if target in data['props']:
        return True
    else:
        return False

async def after_shoot(uid1):
    '''
    消除子弹
    '''
    uid2 = await get_opponent(uid1)
    data_path1 = f'{game_path}/{uid1}.json'
    data_path2 = f'{game_path}/{uid2}.json'
    with open(data_path1, 'r', encoding='utf-8') as f:
        data1 = json.load(f)
    with open(data_path2, 'r', encoding='utf-8') as f:
        data2 = json.load(f)
    data1['bullet'].pop(0)
    data1['handcuffs'] = False
    data1['knife'] = False
    data2['bullet'].pop(0)
    data2['handcuffs'] = False
    data2['knife'] = False
    with open(data_path1, 'w', encoding='utf-8') as f:
        json.dump(data1, f, ensure_ascii=False, indent=4)
    with open(data_path2, 'w', encoding='utf-8') as f:
        json.dump(data2, f, ensure_ascii=False, indent=4)

async def delet_blood(uid, ad):
    """
    扣血
    """
    data_path = f'{game_path}/{uid}.json'
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data['blood'] -= ad
    if data['blood'] == 1 and data['round'] == 3:
        data['heal'] = False
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

async def add_bullet_props(uid1,uid2):
    '''
    补充子弹和道具
    '''
    data_path1 = f'{game_path}/{uid1}.json'
    data_path2 = f'{game_path}/{uid2}.json'
    with open(data_path1, 'r', encoding='utf-8') as f:
        data1 = json.load(f)
    with open(data_path2, 'r', encoding='utf-8') as f:
        data2 = json.load(f)
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
    with open(data_path1, 'w', encoding='utf-8') as f:
        json.dump(data1, f, ensure_ascii=False, indent=4)
    with open(data_path2, 'w', encoding='utf-8') as f:
        json.dump(data2, f, ensure_ascii=False, indent=4)
    return res

async def set_bullet_list(uid1, uid2, bullet_list):
    """
    设置子弹列表
    """
    data_path1 = f'{game_path}/{uid1}.json'
    data_path2 = f'{game_path}/{uid2}.json'
    with open(data_path1, 'r', encoding='utf-8') as f:
        data1 = json.load(f)
    with open(data_path2, 'r', encoding='utf-8') as f:
        data2 = json.load(f)
    data1['bullet'] = bullet_list
    data2['bullet'] = bullet_list
    with open(data_path1, 'w', encoding='utf-8') as f:
        json.dump(data1, f, ensure_ascii=False, indent=4)
    with open(data_path2, 'w', encoding='utf-8') as f:
        json.dump(data2, f, ensure_ascii=False, indent=4)

async def set_handcuffs_type(uid, handcuffs_type):
    '''
    设置手铐的使用状态(该函数暂时不做调用)
    '''
    data_path = f'{game_path}/{uid}.json'
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data['handcuffs'] = handcuffs_type
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)