from nonebot import on_command,on_request
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, Message, GroupMessageEvent,MessageEvent,PrivateMessageEvent,FriendRequestEvent,GroupRequestEvent
from nonebot.params import CommandArg
from nonebot import require
import asyncio

self_add=on_request(priority=60)
group_add=on_request(priority=60)

@self_add.handle()
async def ad_f(bot: Bot, event: FriendRequestEvent):
    await event.approve(bot)
    id = int(event.get_user_id())
    await asyncio.sleep(1)
    await bot.call_api('send_private_msg',user_id=id,message=Message('''---koishi bot---
除today及update外，指令后加空格加数字可指定查询比赛数量，默认查询3场比赛，因缓存原因建议数字<=20
括号内是指令别名
luogu/preluogu（洛谷/洛谷历史）
cf/precf
atc/preatc
nc/prenc（牛客/牛客历史）
today（今日/今日比赛/今天/今天比赛）
next（最近/最近比赛）
update（手动更新）
help
'''
    ))

@group_add.handle()
async def ad_f(bot: Bot, event: GroupRequestEvent):
    await event.approve(bot)
    await asyncio.sleep(1)
