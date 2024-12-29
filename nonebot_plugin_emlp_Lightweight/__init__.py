"""

开局3道具，后续4道具

三回合，前两回合3血，最后一回合4血（1血无法使用回复道具

每次补充子弹，4~8颗，随机虚实子弹

道具列表：
["小刀","华子","饮料","手机","骰子","手铐","偷偷","过期药","放大镜","逆转器"]

"""
from .emlp_rule import *
from .round_action import *
from .user_action import *
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="恶魔轮盘轻量版",
    description="该插件为用户提供基础的游戏逻辑，但需要用户调用该插件提供的函数，自己进行传参和交互反馈的制作，不拘泥于个人开发者的风格",
    usage="参考项目的readme",

    type="application",
    # 发布必填，当前有效类型有：`library`（为其他插件编写提供功能），`application`（向机器人用户提供功能）。

    homepage="https://github.com/STESmly/nonebot_plugin_emlp_Lightweight",
    # 发布必填。

    supported_adapters=None,
    # 支持的适配器集合，其中 `~` 在此处代表前缀 `nonebot.adapters.`，其余适配器亦按此格式填写。
    # 若插件可以保证兼容所有适配器（即仅使用基本适配器功能）可不填写，否则应该列出插件支持的适配器。
)


main_action_list = {
    'shoot' : shoot_action,
    'use' : use_prop,
    'use_steal' : use_steal_prop
}

async def game_run(uid1, uid2):
    """
    创建游戏
    """
    data = await check_user(uid1, uid2)
    if data['type'] == True:
        props1,props2 = await props_at(3)
        bullet = await get_bullet()
        await set_all_blood(uid1, uid2, 3)
        res = await save_bullet_props(uid1, uid2, bullet, props1, props2)
        first_act = await get_frist_act(uid1, uid2)
        res['round'] = 1
        res['first'] = first_act
        res.update(data)
        res = EmlpEvent(**res)
        return res
    else:
        res = EmlpEvent(**data)
        return res
    
async def game_action(uid,action,terget):
    '''
    玩家行动的参数\n
    uid: 玩家id\n
    action: 玩家行动\n
    - shoot: 开枪\n
    - use: 使用道具\n
    - use_steal: 使用偷窃道具\n
    terget: 玩家行动的目标\n
    
    '''
    if await get_user_type(uid):
        uid2 = await get_opponent(uid)
        if action in main_action_list.keys():
            data = await main_action_list[action](uid,terget)
            res = EmlpEvent(**data)
            return res
            
        else:
            data = {'type':False,'msg':'该操作不存在','user':[uid,uid2]}
            res = EmlpEvent(**data)
            return res
    else:
        data = {'type':False,'msg':'玩家未在游戏中','user':[uid]}
        res = EmlpEvent(**data)
        return res
    
async def game_info(uid):
    """
    获取参与者和对手的所有信息
    """
    if await get_user_type(uid):
        data = await get_game_info(uid)
        res = EmlpEvent(**data)
        return res
    else:
        data = {'type':False,'msg':'玩家未在游戏中','user':[uid]}
        res = EmlpEvent(**data)
        return res