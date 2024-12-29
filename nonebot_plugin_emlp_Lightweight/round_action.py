from .emlp_rule import *
from .else_action import *

"""
{
    "blood" : 0,   ##血量
    "round" : 1,   ##回合数
    "bullet" : [],  ##子弹
    "props" : [],   ##道具
    "heal" : True,   ##是否可以治疗
    "handcuffs" : False,   ##是否使用手铐
    "first_act" : True,   ##是否是先手
    "knife" : False,   ##是否使用小刀
}
"""
async def end_game(uid1,uid2):
    """
    结束游戏
    """
    path1=f'{module_path}/data/user/{uid1}.json'
    path2=f'{module_path}/data/user/{uid2}.json'
    data_path1 = f'{module_path}/data/game/{uid1}.json'
    data_path2 = f'{module_path}/data/game/{uid2}.json'
    json.dump(Initialize2,open(path1,'w',encoding='utf-8'),ensure_ascii=False,indent=4)
    json.dump(Initialize2,open(path2,'w',encoding='utf-8'),ensure_ascii=False,indent=4)
    json.dump(Initialize1,open(data_path1,'w',encoding='utf-8'),ensure_ascii=False,indent=4)
    json.dump(Initialize1,open(data_path2,'w',encoding='utf-8'),ensure_ascii=False,indent=4)


async def set_all_blood(uid1, uid2, blood):
    '''
    设置血量
    '''
    data_path1 = f'{module_path}/data/game/{uid1}.json'
    data_path2 = f'{module_path}/data/game/{uid2}.json'
    data1 = json.load(open(data_path1, 'r', encoding='utf-8'))
    data2 = json.load(open(data_path2, 'r', encoding='utf-8'))
    data1['blood'] = blood
    data2['blood'] = blood
    json.dump(data1, open(data_path1, 'w', encoding='utf-8'),ensure_ascii=False,indent=4)
    json.dump(data2, open(data_path2, 'w', encoding='utf-8'),ensure_ascii=False,indent=4)

async def save_bullet_props(uid1, uid2, bullet, props1, props2):
    '''
    保存子弹和道具
    '''
    data_path1 = f'{module_path}/data/game/{uid1}.json'
    data_path2 = f'{module_path}/data/game/{uid2}.json'
    data1 = json.load(open(data_path1, 'r', encoding='utf-8'))
    data2 = json.load(open(data_path2, 'r', encoding='utf-8'))
    data1['bullet'] = bullet
    data1['props'] = props1
    data2['bullet'] = bullet
    data2['props'] = props2
    json.dump(data1, open(data_path1, 'w', encoding='utf-8'),ensure_ascii=False,indent=4)
    json.dump(data2, open(data_path2, 'w', encoding='utf-8'),ensure_ascii=False,indent=4)
    res = {
        'user' : [uid1,uid2],
        'props' : {
            f'{uid1}' : props1,
            f'{uid2}' : props2
        },
        'bullet' : {
            '实弹': bullet.count('实弹'),
            '空弹': bullet.count('空弹')
        }
    }
    return res

async def change_round(uid1, uid2):
    '''
    改变回合
    '''
    data_path1 = f'{module_path}/data/game/{uid1}.json'
    data_path2 = f'{module_path}/data/game/{uid2}.json'
    data1 = json.load(open(data_path1, 'r', encoding='utf-8'))
    data2 = json.load(open(data_path2, 'r', encoding='utf-8'))
    data1['round'] += 1
    data2['round'] += 1
    round = data1['round']
    if data1['round'] <= 2:
        data1['blood'] = 3
        data2['blood'] = 3
    elif data1['round'] == 3:
        data1['blood'] = 4
        data2['blood'] = 4
    else:
        await end_game(uid1, uid2)
        return True, { 'type' : False, 'msg' : '游戏结束','user': [uid1,uid2] }
    props1,props2 = await props_at(3)
    bullet = await get_bullet()
    data1['bullet'] = bullet
    data1['props'] = props1
    data2['bullet'] = bullet
    data2['props'] = props2
    res = {
        'user' : [uid1,uid2],
        'props' : {
            f'{uid1}' : props1,
            f'{uid2}' : props2
        },
        'bullet' : {
            '实弹': bullet.count('实弹'),
            '空弹': bullet.count('空弹')
        },
        'round' : round,
        'status_up' : True
    }
    json.dump(data1, open(data_path1, 'w', encoding='utf-8'),ensure_ascii=False,indent=4)
    json.dump(data2, open(data_path2, 'w', encoding='utf-8'),ensure_ascii=False,indent=4)
    return False, res