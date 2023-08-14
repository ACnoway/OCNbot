from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, Message, GroupMessageEvent,MessageEvent,PrivateMessageEvent
from nonebot.params import CommandArg
from nonebot import require
import time

help=on_command('help', priority=1)

@help.handle()
async def send_receive(bot: Bot, event: MessageEvent):
    res='''除today及update外，指令后加空格加数字可指定查询比赛数量，默认查询3场比赛，因缓存原因建议数字<=20
括号内是指令别名
luogu/preluogu（洛谷/洛谷历史）
cf/precf
atc/preatc
nc/prenc（牛客/牛客历史）
today（今日/今日比赛/今天/今天比赛）
next（最近/最近比赛）
update（手动更新）
help
'''+"\n\n防风控编码"+str(time.time())
    await help.finish(res)