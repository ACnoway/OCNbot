# 手动更新

from nonebot import on_command,logger
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, Message, GroupMessageEvent,MessageEvent,PrivateMessageEvent
from nonebot.params import CommandArg
import requests
import json

update=on_command('update', priority=1, aliases={'手动更新'})

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

@update.handle()
async def send_receive(bot: Bot, event: MessageEvent):
    await get_luogu()
    await get_cf()
    await get_atc()
    await get_nowcoder()
    await update.finish("更新成功")

async def get_luogu():
    # 这里简单返回一个字符串
    # 实际应用中，这里应该调用返回 luogu 的 API
    response=requests.get("https://www.luogu.com.cn/contest/list?_contentOnly=any",timeout=10,headers=headers)
    res=response.text
    pos=res.find("\"code\":200")
    if pos==-1: return
    # res=json.dumps(response.json())
    f=open('luogu.txt','w',encoding='utf-8')
    f.write(res)
    f.close()
    
async def get_cf():
    # 这里简单返回一个字符串
    # 实际应用中，这里应该调用返回 cf 的 API
    response=requests.get("https://codeforces.com/api/contest.list?gym=false",timeout=10,headers=headers)
    res=response.text
    pos=res.find("unavailable")
    if pos!=-1: return
    res=json.dumps(response.json())
    f=open('cf.txt','w',encoding='utf-8')
    f.write(res)
    f.close()

async def get_atc():
    # 这里简单返回一个字符串
    # 实际应用中，这里应该调用返回 cf 的 API
    response=requests.get("https://atcoder.jp/contests/",timeout=10,headers=headers)
    res=response.text
    f=open('atc.txt','w',encoding='utf-8')
    f.write(res)
    f.close()

async def get_nowcoder():
    # 这里简单返回一个字符串
    # 实际应用中，这里应该调用返回 cf 的 API
    response=requests.get("https://ac.nowcoder.com/acm/contest/vip-index",timeout=10,headers=headers)
    res=response.text
    f=open('nc.txt','w',encoding='utf-8')
    f.write(res)
    f.close()