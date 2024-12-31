from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class EmlpEvent(BaseModel):
    user: List[int]
    """事件参与者们的唯一标识（例如：参与者的QQ号）\n
    [int, int]
    """
    msg: Optional[str] = Field(None, description="触发该事件的结果的描述（慎用，通常无法作为判断使用，仅有反馈文本的用途，因为内容不统一）")
    thebullet: Optional[str] = Field(None, description="事件中涉及的子弹类型，例如开枪，使用饮料，放大镜等")
    first_change: Optional[int] = Field(None, description="在事件结束后先手者的唯一标识（例如：参与者的QQ号）")
    hurt: Optional[int] = Field(None, description="""
    事件中造成的伤害
        - 开枪事件 : 为扣血伤害
        - 治疗道具事件 : 正数为治疗伤害，负数为毒药伤害
    """)
    props: Optional[Dict[str, List[str]]] = Field(None, description="""
    事件参与者们的道具信息\n
    {str(uid1) : [str(props1), props2, ...], str(uid2) : [str(props1), props2, ...]}
    """)
    bullet: Optional[Dict[str, List[str]]] = Field(None, description="""
    事件参与者们的子弹信息\n
    {str(uid1) : [str(bullet1), bullet2, ...], str(uid2) : [bullet1, bullet2, ...]}
    """)
    round: Optional[int] = Field(None, description="当前的回合")
    first: Optional[int] = Field(None, description="当前回合先手者的唯一标识（例如：参与者的QQ号）")
    type: bool = Field(True, description="""
    事件类型
        - False : 该事件请求驳回
        - True : 该事件请求通过
    """)
    blood: Optional[Dict[str, int]] = Field(None, description="""
    事件结束后参与者们的血量信息\n
    {str(uid1) : int(blood1), str(uid2) : int(blood2)}
    """)
    status_up: bool = Field(False, description="""
    事件结束后是否需要重新更新子弹，道具等状态版
        - True : 需要更新
        - False : 不需要更新
    """)
    use_phone: Optional[int] = Field(None, description="使用手机道具事件中，得知的第几颗子弹的子弹类型")
    private_type: bool = Field(False, description="""
    事件结果是否为需要私聊反馈
        - True : 需要私聊反馈
        - False : 不需要私聊反馈
    """)

    class Config:
        extra = "allow"