import json
import os
from pathlib import Path
module_path: Path = Path(__file__).parent


async def get_opponent(uid):
    '''
    获取对手
    '''
    data_path = f'{module_path}/data/user/{uid}.json'
    data = json.load(open(data_path, 'r', encoding='utf-8'))
    return data['opponent']

async def check_first_act(uid):
    '''
    检查是否是先手
    '''
    data_path = f'{module_path}/data/game/{uid}.json'
    data = json.load(open(data_path, 'r', encoding='utf-8'))
    if data['first_act'] == True:
        return True
    else:
        return False
    
async def get_props_list(uid):
    '''
    获取道具列表
    '''
    data_path = f'{module_path}/data/game/{uid}.json'
    data = json.load(open(data_path, 'r', encoding='utf-8'))
    return data['props']

async def get_bullet_list(uid):
    '''
    获取子弹列表
    '''
    data_path = f'{module_path}/data/game/{uid}.json'
    data = json.load(open(data_path, 'r', encoding='utf-8'))
    return data['bullet']

async def get_round(uid):
    '''
    获取回合数
    '''
    data_path = f'{module_path}/data/game/{uid}.json'
    data = json.load(open(data_path, 'r', encoding='utf-8'))
    return data['round']

async def get_game_info(uid):
    """
    获取所有相关信息
    """
    uid2 = await get_opponent(uid)
    blood1 = await get_blood(uid)
    blood2 = await get_blood(uid2)
    if await check_first_act(uid):
        first_act = uid
    else:
        first_act = uid2
    props1 = await get_props_list(uid)
    props2 = await get_props_list(uid2)
    round = await get_round(uid)
    data = {
        'user' : [uid, uid2],
        'blood' : {
            f'{uid}':blood1,
            f'{uid2}':blood2
        },
        'first': first_act,
        'props' : {
            f'{uid}':props1,
            f'{uid2}':props2
        },
        'round': round
    }
    return data
    
    

async def get_blood(uid):
    '''
    获取血量
    '''
    data_path = f'{module_path}/data/game/{uid}.json'
    data = json.load(open(data_path, 'r', encoding='utf-8'))
    return data['blood']

async def get_handcuffs_type(uid):
    '''
    获取手铐的使用状态
    '''
    data_path = f'{module_path}/data/game/{uid}.json'
    data = json.load(open(data_path, 'r', encoding='utf-8'))
    return data['handcuffs']

async def get_knife_type(uid):
    '''
    获取小刀的使用状态
    '''
    data_path = f'{module_path}/data/game/{uid}.json'
    data = json.load(open(data_path, 'r', encoding='utf-8'))
    return data['knife']

async def get_heal_type(uid):
    '''
    获取治疗药是否能使用
    '''
    data_path = f'{module_path}/data/game/{uid}.json'
    data = json.load(open(data_path, 'r', encoding='utf-8'))
    return data['heal']

async def get_user_type(uid):
    '''
    获取用户游戏状态
    '''
    path=f'{module_path}/data/user/{uid}.json'
    if os.path.exists(path):
        data = json.load(open(path, 'r', encoding='utf-8'))
        if data['status'] == '游戏中':
            return True
        else:
            return False
    else:
        return False