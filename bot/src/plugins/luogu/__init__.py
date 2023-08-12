from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, Message, GroupMessageEvent,MessageEvent,PrivateMessageEvent
from nonebot.params import CommandArg
import time
import json
luogu=on_command('luogu', priority=1, aliases={"洛谷"}, force_whitespace=True)
preluogu=on_command('preluogu', priority=1, aliases={"洛谷历史"}, force_whitespace=True)

@luogu.handle()
async def send_receive(bot: Bot, event: MessageEvent):
    try:
        counts = int(str(event.get_message()).split()[1])
    except:
        counts = 3
    res=await get_luogu(counts)
    await luogu.finish(res)

@preluogu.handle()
async def send_receive(bot: Bot, event: MessageEvent):
    try:
        counts = int(str(event.get_message()).split()[1])
    except:
        counts = 3
    res=await get_preluogu(counts)
    await preluogu.finish(res)

async def get_luogu(counts):
    results = []
    
    f = open('luogu.txt', 'r',encoding='utf-8')
    res = f.read()
    f.close()
    res = json.loads(res)['currentData']['contests']['result']
    for ress in res:
        if ress['endTime'] < time.time():
            break
        name=ress['name']
        DateTime=ress['startTime']
        contest_id=ress['id']
        time_local=time.localtime(DateTime)
        dt=time.strftime("%Y-%m-%d %H:%M:%S",time_local)
        # 加入队列中：名称，时间，id
        results.insert(0,[name,dt,str(contest_id)])
        if len(results) >= counts:
            break
    if len(results)==0:
        return "没有找到要开始的洛谷比赛哦"
    else:
        ans=""
        for conts in results:
            ans+="\n\n比赛名称："+conts[0]
            ans+="\n比赛时间："+conts[1]
            ans+="\n比赛链接：https://www.luogu.com.cn/contest/"+conts[2]
        if len(results) < counts:
            return '洛谷最近比赛不足 '+str(counts)+'场，找到最近的 '+str(len(results))+' 场比赛如下：'+ans
        else:
            return '找到最近的 '+str(len(results))+' 场洛谷比赛如下：'+ans

async def get_preluogu(counts):
    results = []
    
    f = open('luogu.txt', 'r',encoding='utf-8')
    res = f.read()
    f.close()
    res = json.loads(res)['currentData']['contests']['result']
    for ress in res:
        if ress['endTime'] > time.time():
            continue
        name=ress['name']
        DateTime=ress['startTime']
        contest_id=ress['id']
        time_local=time.localtime(DateTime)
        dt=time.strftime("%Y-%m-%d %H:%M:%S",time_local)
        # 加入队列中：名称，时间，id
        results.append([name,dt,str(contest_id)])
        if len(results) >= counts:
            break
    if len(results)==0:
        return "居然找不到，可能是：\n1. bot裂了\n2. 网站裂了\n3. 缓存裂了\n4. 地球裂了"
    else:
        ans=""
        for conts in results:
            ans+="\n\n比赛名称："+conts[0]
            ans+="\n比赛时间："+conts[1]
            ans+="\n比赛链接：https://www.luogu.com.cn/contest/"+conts[2]
        if len(results) < counts:
            return '缓存中洛谷历史比赛不足 '+str(counts)+'场，找到历史 '+str(len(results))+' 场比赛如下：'+ans
        else:
            return '找到历史 '+str(len(results))+' 场洛谷比赛如下：'+ans