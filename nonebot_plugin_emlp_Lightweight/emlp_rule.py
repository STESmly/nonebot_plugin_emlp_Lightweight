import random,json,os
from pathlib import Path

Initialize = {
    "blood" : 0,   ##血量
    "round" : 1,   ##回合数
    "bullet" : [],  ##子弹
    "props" : [],   ##道具
    "heal" : True,   ##是否可以治疗
    "handcuffs" : False,   ##是否使用手铐
    "first_act" : True,   ##是否是先手
    "knife" : False,   ##是否使用小刀
}
module_path: Path = Path(__file__).parent
props_probability = {"小刀":2,"华子":2,"饮料":2,"手机":2,"骰子":1,"手铐":2,"偷偷":2,"过期药":2,"放大镜":2,"逆转器":2}
async def props_at(num_items:int,probability=props_probability):
    """
    回合开始时分发道具
    uid:用户id
    num_items:分发道具数量
    """
    prop_list = list(probability.keys())
    prob_list = list(probability.values())

    # 随机选择道具列表
    prop1 = random.choices(prop_list, weights=prob_list, k=num_items)
    prop2 = random.choices(prop_list, weights=prob_list, k=num_items)
    return prop1,prop2

async def get_bullet():
    '''
    获取子弹
    uid:用户id
    '''
    num = random.randint(4,8)
    bullets = random.choices(['实弹','空弹'],k=num)
    if bullets.count('实弹') == len(bullets) or bullets.count('空弹') == len(bullets):
        # 随机选择1到2个位置进行替换
        num_to_replace = random.randint(1, 2)
        for _ in range(num_to_replace):
            index = random.randint(0, len(bullets) - 1)
            bullets[index] = '空弹' if bullets[index] == '实弹' else '实弹'   
    return bullets

async def get_frist_act(uid1,uid2):
    '''
    谁先行动
    '''
    first = random.choice([uid1,uid2])
    data_path1 = f'{module_path}/data/game/{uid1}.json'
    data_path2 = f'{module_path}/data/game/{uid2}.json'
    data1 = json.load(open(data_path1, 'r', encoding='utf-8'))
    data2 = json.load(open(data_path2, 'r', encoding='utf-8'))
    if first == uid1:
        data1['first_act'] = True
        data2['first_act'] = False
    else:
        data1['first_act'] = False
        data2['first_act'] = True
    json.dump(data1, open(data_path1, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
    json.dump(data2, open(data_path2, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
    return first


async def check_user(uid1,uid2):
    '''
    检查用户是否在游戏中
    uid:用户id
    '''
    path1=f'{module_path}/data/user/{uid1}.json'
    path2=f'{module_path}/data/user/{uid2}.json'
    data_path1 = f'{module_path}/data/game/{uid1}.json'
    data_path2 = f'{module_path}/data/game/{uid2}.json'
    if os.path.exists(path1):
        data1 = json.load(open(path1,'r',encoding='utf-8'))
        if os.path.exists(path2):
            data2 = json.load(open(path2,'r',encoding='utf-8'))
            if data1['status'] == '游戏中' and data2['status'] == '游戏中':
                data = {
                    'user': [uid1,uid2],
                    'type': False,
                    'msg': '在游戏中',
                }
                return data
            elif data1['status'] == '游戏中' and data2['status'] != '游戏中':
                data = {
                    'user': [uid1],
                    'type': False,
                    'msg': '在游戏中',
                }
                return data
            elif data1['status'] != '游戏中' and data2['status'] == '游戏中':
                data = {
                    'user': [uid2],
                    'type': False,
                    'msg': '在游戏中',
                }
                return data
            else:
                data = {
                    'user': [uid1,uid2],
                    'type': True,
                    'msg': '开始对局',
                }
                data1['status'] = '游戏中'
                data1['opponent'] = uid2
                data2['status'] = '游戏中'
                data2['opponent'] = uid1
                json.dump(data1,open(path1,'w',encoding='utf-8'),ensure_ascii=False,indent=4)
                json.dump(data2,open(path2,'w',encoding='utf-8'),ensure_ascii=False,indent=4)
                return data
        else:
            if data1['status'] == '游戏中':
                data = {
                    'user': [uid1],
                    'type': False,
                    'msg': '在游戏中',
                }
                return data
            else:
                data = {
                    'user': [uid1,uid2],
                    'type': True,
                    'msg': '开始对局',
                }
                data1['status'] = '游戏中'
                data1['opponent'] = uid2
                data2 = {
                    'status' : '游戏中',
                    'opponent' : uid1
                }
                json.dump(data1,open(path1,'w',encoding='utf-8'),ensure_ascii=False,indent=4)
                json.dump(data2,open(path2,'w',encoding='utf-8'),ensure_ascii=False,indent=4)
                json.dump(Initialize,open(data_path2,'w',encoding='utf-8'),ensure_ascii=False,indent=4)
                return data
    elif os.path.exists(path2):
        data2 = json.load(open(path2,'r',encoding='utf-8'))
        if os.path.exists(path1):
            data1 = json.load(open(path1,'r',encoding='utf-8'))
            if data2['status'] == '游戏中' and data1['status'] == '游戏中':
                data = {
                    'user': [uid1,uid2],
                    'type': False,
                    'msg': '在游戏中',
                }
                return data
            elif data2['status'] == '游戏中' and data1['status'] != '游戏中':
                data = {
                    'user': [uid1],
                    'type': False,
                    'msg': '在游戏中',
                }
                return data
            elif data2['status'] != '游戏中' and data1['status'] == '游戏中':
                data = {
                    'user': [uid2],
                    'type': False,
                    'msg': '在游戏中',
                }
                return data
            else:
                data = {
                    'user': [uid1,uid2],
                    'type': True,
                    'msg': '开始对局',
                }
                data2['status'] = '游戏中'
                data2['opponent'] = uid1
                data1['status'] = '游戏中'
                data1['opponent'] = uid2
                json.dump(data2,open(path2,'w',encoding='utf-8'),ensure_ascii=False,indent=4)
                json.dump(data1,open(path1,'w',encoding='utf-8'),ensure_ascii=False,indent=4)
                return data
        else:
            if data2['status'] == '游戏中':
                data = {
                    'user': [uid1],
                    'type': False,
                    'msg': '在游戏中',
                }
                return data
            else:
                data = {
                    'user': [uid1,uid2],
                    'type': True,
                    'msg': '开始对局',
                }
                data2['status'] = '游戏中'
                data2['opponent'] = uid1
                data1 = {
                    'status' : '游戏中',
                    'opponent' : uid2
                }
                json.dump(data2,open(path2,'w',encoding='utf-8'),ensure_ascii=False,indent=4)
                json.dump(data1,open(path1,'w',encoding='utf-8'),ensure_ascii=False,indent=4)
                json.dump(Initialize,open(data_path1,'w',encoding='utf-8'),ensure_ascii=False,indent=4)
                return data
    else:
        data = {
            'user': [uid1,uid2],
            'type': True,
            'msg': '开始对局',
        }
        data2 = {
            'status' : '游戏中',
            'opponent' : uid1
        }
        data1 = {
            'status' : '游戏中',
            'opponent' : uid2
        }
        json.dump(data2,open(path2,'w',encoding='utf-8'),ensure_ascii=False,indent=4)
        json.dump(data1,open(path1,'w',encoding='utf-8'),ensure_ascii=False,indent=4)
        json.dump(Initialize,open(data_path2,'w',encoding='utf-8'),ensure_ascii=False,indent=4)
        json.dump(Initialize,open(data_path1,'w',encoding='utf-8'),ensure_ascii=False,indent=4)
        return data