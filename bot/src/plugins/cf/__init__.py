from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, Message, GroupMessageEvent,MessageEvent,PrivateMessageEvent
from nonebot.params import CommandArg
import time
import json
cf=on_command('cf', priority=1, force_whitespace=False)
precf=on_command('precf', priority=1, force_whitespace=False)

@cf.handle()
async def send_receive(bot: Bot, event: MessageEvent):
    try:
        counts = int(str(event.get_message()).split()[1])
    except:
        counts = 3
    res=await get_cf(counts)
    await cf.finish(res)

@precf.handle()
async def send_receive(bot: Bot, event: MessageEvent):
    try:
        counts = int(str(event.get_message()).split()[1])
    except:
        counts = 3
    res=await get_precf(counts)
    await precf.finish(res)

async def get_cf(counts):
    results = []
    
    # response=requests.get("https://codeforces.com/api/contest.list?gym=false")
    f = open('cf.txt', 'r',encoding='utf-8')
    res = f.read()
    f.close()
    res = json.loads(res)['result']
    for ress in res:
        if ress["phase"] == "FINISHED":
            break
        name=ress['name']
        DateTime=ress['startTimeSeconds']
        contest_id=ress['id']
        time_local=time.localtime(DateTime)
        dt=time.strftime("%Y-%m-%d %H:%M:%S",time_local)
        # 加入队列中：名称，时间，id
        results.insert(0,[name,dt,str(contest_id)])
        if len(results) >= counts:
            break
    if len(results)==0:
        return "没有找到要开始的codeforces比赛哦"
    else:
        ans=""
        for conts in results:
            ans+="\n\n比赛名称："+conts[0]
            ans+="\n比赛时间："+conts[1]
            ans+="\n比赛链接：https://codeforces.com/contest/"+conts[2]
        if len(results) < counts:
            return 'codeforces最近比赛不足 '+str(counts)+'场，找到最近的 '+str(len(results))+' 场比赛如下：'+ans
        else:
            return '找到最近的 '+str(len(results))+' 场codeforces比赛如下：'+ans

async def get_precf(counts):
    results = []
    
    f = open('cf.txt', 'r',encoding='utf-8')
    res = f.read()
    f.close()
    res = json.loads(res)['result']
    for ress in res:
        if ress["phase"] != "FINISHED":
            continue
        name=ress['name']
        DateTime=ress['startTimeSeconds']
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
            ans+="\n比赛链接：https://codeforces.com/contest/"+conts[2]
        if len(results) < counts:
            return '缓存中codeforces历史比赛不足 '+str(counts)+'场，找到历史 '+str(len(results))+' 场比赛如下：'+ans
        else:
            return '找到历史 '+str(len(results))+' 场codeforces比赛如下：'+ans