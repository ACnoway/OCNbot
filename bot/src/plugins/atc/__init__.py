from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, Message, GroupMessageEvent,MessageEvent,PrivateMessageEvent
from nonebot.params import CommandArg
import time
from bs4 import BeautifulSoup
import datetime
atc=on_command('atc', priority=1, force_whitespace=True)
preatc=on_command('preatc', priority=1, force_whitespace=True)

@atc.handle()
async def send_receive(bot: Bot, event: MessageEvent):
    try:
        counts = int(str(event.get_message()).split()[1])
    except:
        counts = 3
    res=await get_atc(counts)
    await atc.finish(res)

@preatc.handle()
async def send_receive(bot: Bot, event: MessageEvent):
    try:
        counts = int(str(event.get_message()).split()[1])
    except:
        counts = 3
    res=await get_preatc(counts)
    await preatc.finish(res)

async def get_atc(counts):
    results=[]
    
    # response=requests.get("https://ac.atc.com/acm/contest/vip-index")
    # res=response.text
    f=open('atc.txt','r',encoding='utf-8')
    res=f.read()
    f.close()
    res = BeautifulSoup(res, "html.parser")
    res = res.select('#contest-table-upcoming tbody tr')
    for ress in res:
        name=ress.select('a')[1].text
        DateTime=ress.select('time')[0].text
        last=DateTime.find("+",0)
        DateTime=DateTime[0:last]
        contest_id=ress.select('a')[1]['href']
        time_local=datetime.datetime.strptime(DateTime,'%Y-%m-%d %H:%M:%S')
        time_local-=datetime.timedelta(hours=1)
        dt=datetime.datetime.strftime(time_local,'%Y-%m-%d %H:%M:%S')
        # 加入队列中：名称，时间，id
        results.append([name,dt,contest_id])
        if len(results) >= counts:
            break
    if len(results)==0:
        return "没有找到要开始的atcoder比赛哦"
    else:
        ans=""
        for conts in results:
            ans+="\n\n比赛名称："+conts[0]
            ans+="\n比赛时间："+conts[1]
            ans+="\n比赛链接：https://atcoder.jp"+conts[2]
        if len(results) < counts:
            return 'atcoder最近比赛不足 '+str(counts)+'场，找到最近的 '+str(len(results))+' 场比赛如下：'+ans
        else:
            return '找到最近的 '+str(len(results))+' 场atcoder比赛如下：'+ans

async def get_preatc(counts):
    results=[]
    
    f=open('atc.txt','r',encoding='utf-8')
    res=f.read()
    f.close()
    res = BeautifulSoup(res, "html.parser")
    res = res.select('#contest-table-recent tbody tr')
    for ress in res:
        name=ress.select('a')[1].text
        DateTime=ress.select('time')[0].text
        last=DateTime.find("+",0)
        DateTime=DateTime[0:last]
        contest_id=ress.select('a')[1]['href']
        time_local=datetime.datetime.strptime(DateTime,'%Y-%m-%d %H:%M:%S')
        time_local-=datetime.timedelta(hours=1)
        dt=datetime.datetime.strftime(time_local,'%Y-%m-%d %H:%M:%S')
        # 加入队列中：名称，时间，id
        results.append([name,dt,contest_id])
        if len(results) >= counts:
            break
    if len(results)==0:
        return "居然找不到，可能是：\n1. bot裂了\n2. 网站裂了\n3. 缓存裂了\n4. 地球裂了"
    else:
        ans=""
        for conts in results:
            ans+="\n\n比赛名称："+conts[0]
            ans+="\n比赛时间："+conts[1]
            ans+="\n比赛链接：https://atcoder.jp"+conts[2]
        if len(results) < counts:
            return '缓存中atcoder历史比赛不足 '+str(counts)+'场，找到历史 '+str(len(results))+' 场比赛如下：'+ans
        else:
            return '找到历史 '+str(len(results))+' 场atcoder比赛如下：'+ans
