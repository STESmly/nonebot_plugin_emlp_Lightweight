<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot_plugin_emlp_Lightweight

_✨ NoneBot 插件描述 ✨_

这是一个轻量级的恶魔轮盘插件，没有平台适配限制，插件只提供基础交互逻辑，指令，反馈这些的交给用户自己去编写
</div>

## 📖 介绍

在原版恶魔轮盘的基础上加入了一些自己加入的道具

每回合开局3道具，后续4道具

三回合，前两回合3血，最后一回合4血（1血无法使用回复道具）

每次补充子弹，4~8颗，随机虚实子弹

## 道具说明

| 道具 | 出现的概率 | 作用 |
|:-----:|:----:|:----:|
| 小刀 | 10.52% | 实弹加1子弹伤害 |
| 华子 | 10.52% | 回复1滴血 |
| 饮料 | 10.52% | 退掉当前的子弹 |
| 手机 | 10.52% | 得知从当前开始第n颗子弹的类型 |
| 骰子 | 5.26% | 打乱剩余子弹的顺序 |
| 手铐 | 10.52% | 禁止对手行动1回合 |
| 偷偷 | 10.52% | 偷走对方指定道具并立即使用 |
| 过期药 | 10.52% | 50%回复2滴血，50%扣除1滴血 |
| 放大镜 | 10.52% | 得知当前的子弹的类型 |
| 逆转器 | 10.52% | 反转当前子弹类型 |

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot_plugin_emlp_Lightweight

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot_plugin_emlp_Lightweight
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_emlp_Lightweight"]

</details>

## 示例代码


```bash

from nonebot import require
require("nonebot_plugin_emlp_Lightweight")
from nonebot_plugin_emlp_Lightweight import (
    game_run,
    game_action,
    game_info,
    end_game
)
from nonebot.adapters.onebot.v11 import MessageSegment,GroupMessageEvent,Event, PrivateMessageEvent,Message,Bot,FriendRequestEvent
from nonebot import on_command,on_request
from nonebot.params import CommandArg

async def check_user_QQ(uid1, uid2):
    (bot,) = nonebot.get_bots().values()
    try:
        await bot.send_private_msg(user_id=uid1, message='这是一条验证是否为好友的消息，无需在意')
        data1 = True
    except nonebot.adapters.onebot.v11.exception.ActionFailed:
        data1 = False
    try:
        await bot.send_private_msg(user_id=uid2, message='这是一条验证是否为好友的消息，无需在意')
        data2 = True
    except nonebot.adapters.onebot.v11.exception.ActionFailed:
        data2 = False
    return data1 , data2

game_run_gb = on_command("创建对局")
game_user_action_shoot = on_command("开枪")
game_user_action_use_props_toutou = on_command("使用偷偷",block=True)
game_user_action_use_props = on_command("使用")
game_user_info = on_command("信息")
game_end = on_command("结束对局")

def friend_event(event: Event):
    return isinstance(event, FriendRequestEvent)

friend_add_event=on_request(rule=friend_event)
@friend_add_event.handle()
async def friend_request_handle(bot: Bot, event: FriendRequestEvent):
    await bot.set_friend_add_request(flag=event.flag, approve=True)
    await bot.send_private_msg(user_id=event.user_id, message='已自动通过你的好友申请')


@game_run_gb.handle()
async def _(event: GroupMessageEvent):
    if len(at := event.original_message.include("at")) > 0:
        id = int(at[0].data["qq"])
        data1,data2 = await check_user_QQ(event.user_id,id)
        if data1 and data2:
            data = await game_run(event.user_id,id)
            if data.type:
                ##这边就是创建对局成功之后的反馈
            else:
                await game_run_gb.finish(data.msg) ###这个是创建对局请求被驳回之后的反馈
        else:
            if data1 == False and data2 == False:
                await game_run_gb.send(MessageSegment.at(event.user_id)+"和"+MessageSegment.at(id)+"请加我为好友再创建对局，否则将无法进行正常对局（因为非好友状态使用手机道具会失效）")
            elif data1 == False:
                await game_run_gb.send(MessageSegment.at(event.user_id)+"请加我为好友再创建对局，否则将无法进行正常对局（因为非好友状态使用手机道具会失效）")
            elif data2 == False:
                await game_run_gb.send(MessageSegment.at(id)+"请加我为好友再创建对局，否则将无法进行正常对局（因为非好友状态使用手机道具会失效）")

@game_user_action_shoot.handle()
async def _(event: GroupMessageEvent,args: Message = CommandArg()):
    if args.extract_plain_text() == '对己' or args.extract_plain_text() == 'me':
        target = 'self'
    elif args.extract_plain_text() == '对敌' or args.extract_plain_text() == 'enemy':
        target = 'opponent'   ##这边将射击的操作转为对应的目标参数
    emlp = await game_action(event.user_id,'shoot',target)   ##这边的'shoot'为行动类型
    if emlp.type:
        ##开枪事件结束后的反馈
        if emlp.status_up:
            ##这代表你要更新局内双方的状态版了
    else:
        await game_user_action_shoot.finish(str(emlp.msg))

@game_user_action_use_props_toutou.handle()
async def _(event: GroupMessageEvent,bot:Bot, args:Message =  CommandArg()):
    target = args.extract_plain_text()
    emlp = await game_action(event.user_id,'use_steal',target) ##这边的'use_steal'为行动类型，指代使用特殊道具偷偷 ，target为道具名称
    if emlp.type:
        if emlp.private_type:  ##判断是否需要私聊发送
            await bot.send_private_msg(user_id=event.user_id,message=MessageSegment.text('道具：'+target+'\n'+emlp.msg))
        else:
            await game_user_action_use_props.send(MessageSegment.text('道具：'+target+'\n'+emlp.msg))
        if emlp.status_up:
            ##这代表你要更新局内双方的状态版了
    else:
        await game_user_action_use_props.send(emlp.msg)

@game_user_action_use_props.handle()
async def _(event: GroupMessageEvent,bot:Bot, args:Message =  CommandArg()):
    target = args.extract_plain_text()
    emlp = await game_action(event.user_id,'use',target)
    if emlp.type:
        if emlp.private_type:
            await bot.send_private_msg(user_id=event.user_id,message=MessageSegment.text('道具：'+target+'\n'+emlp.msg ))
        else:
                await game_user_action_use_props.send(MessageSegment.text('道具：'+target+'\n'+emlp.msg))
        if emlp.status_up:
            ##这代表你要更新局内双方的状态版了
    else:
        await game_user_action_use_props.send(emlp.msg)

        
@game_user_info.handle()
async def _(event: GroupMessageEvent):
    emlp = await game_info(event.user_id)
    if emlp.type:
        ## 这里是获取双方信息的
    else:
        await game_user_info.send(emlp.msg)

@game_end.handle()
async def _(event: GroupMessageEvent):
    if len(at := event.original_message.include("at")) > 0:
        id = int(at[0].data["qq"])
        await end_game(event.user_id,id)
        await game_end.send(MessageSegment.text("游戏结束"))
```

## 具体的返回数据的类型
```bash
    user: list
    """事件参与者们的唯一标识（例如：参与者的QQ号）\n
    [int, int]
    """
    msg: str = None
    """触发该事件的结果的描述（慎用，通常无法作为判断使用，仅有反馈文本的用途，因为内容不统一）"""
    thebullet: str = None
    """事件中涉及的子弹类型，例如开枪，使用饮料，放大镜等"""
    first_change: int = None
    """在事件结束后先手者的唯一标识（例如：参与者的QQ号）"""
    hurt: int = None
    """
    事件中造成的伤害
        - 开枪事件 : 为扣血伤害
        - 治疗道具事件 : 正数为治疗伤害，负数为毒药伤害
    """
    props: dict = None
    """
    事件参与者们的道具信息\n
    {str(uid1) : [str(props1), props2, ...], str(uid2) : [str(props1), props2, ...]}
    """
    bullet: dict = None
    """
    事件参与者们的子弹信息\n
    {str(uid1) : [str(bullet1), bullet2, ...], str(uid2) : [bullet1, bullet2, ...]}
    """
    round: int = None
    """当前的回合"""
    first : int = None
    """当前回合先手者的唯一标识（例如：参与者的QQ号）"""
    type: bool = True
    """事件类型
        - False : 该事件请求驳回
        - True : 该事件请求通过
    """
    blood: dict = None
    """
    事件结束后参与者们的血量信息\n
    {str(uid1) : int(blood1), str(uid2) : int(blood2)}
    """
    status_up:bool = False
    """
    事件结束后是否需要重新更新子弹，道具等状态版
        - True : 需要更新
        - False : 不需要更新
    """
    use_phone: int = None
    """使用手机道具事件中，得知的第几颗子弹的子弹类型"""
    private_type: bool = False
    """
    事件结果是否为需要私聊反馈
        - True : 需要私聊反馈
        - False : 不需要私聊反馈
    """
```