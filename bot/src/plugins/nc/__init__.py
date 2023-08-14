from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, Message, GroupMessageEvent,MessageEvent,PrivateMessageEvent
from nonebot.params import CommandArg
import time
from bs4 import BeautifulSoup
import datetime
nc=on_command('nc', priority=1, aliases={"牛客"}, force_whitespace=False)
prenc=on_command('prenc', priority=1, aliases={"牛客历史"}, force_whitespace=False)

@nc.handle()
async def send_receive(bot: Bot, event: MessageEvent):
    try:
        counts = int(str(event.get_message()).split()[1])
    except:
        counts = 3
    res=await get_nowcoder(counts)
    await nc.finish(res)

@prenc.handle()
async def send_receive(bot: Bot, event: MessageEvent):
    try:
        counts = int(str(event.get_message()).split()[1])
    except:
        counts = 3
    res=await get_prenowcoder(counts)
    await prenc.finish(res)

async def get_nowcoder(counts):
    results=[]
    
    #* 牛客
    # response=requests.get("https://ac.nowcoder.com/acm/contest/vip-index")
    # res=response.text
    f=open('nc.txt','r',encoding='utf-8')
    res=f.read()
    f.close()
    res = BeautifulSoup(res, "html.parser")
    res = res.select('.platform-mod.js-current .platform-item.js-item')
    for ress in res:
        # 选择比赛介绍
        cont=ress.select('.platform-item-cont')[0]
        name=cont.select('h4 a')[0].text
        DateTime=cont.select('.platform-info .match-time-icon')[0].text
        st=DateTime.find("报名时间： ",0)
        last=DateTime.find("\n",0)
        DateTime=DateTime[st+7:last].strip()
        contest_id=ress.select('h4 a')[0]['href']
        time_local=datetime.datetime.strptime(DateTime,'%Y-%m-%d %H:%M')
        dt=datetime.datetime.strftime(time_local,'%Y-%m-%d %H:%M:%S')
        # 加入队列中：名称，时间，id
        results.append([name,dt,contest_id])
        if len(results) >= counts:
            break
    if len(results)==0:
        return "没有找到要开始的牛客比赛哦"+"\n\n防风控编码"+str(time.time())
    else:
        ans=""
        for conts in results:
            ans+="\n\n比赛名称："+conts[0]
            ans+="\n比赛时间："+conts[1]
            ans+="\n比赛链接：https://ac.nowcoder.com/acm/contest/"+conts[2]
        if len(results) < counts:
            return '牛客最近比赛不足 '+str(counts)+'场，找到最近的 '+str(len(results))+' 场比赛如下：'+ans+"\n\n防风控编码"+str(time.time())
        else:
            return '找到最近的 '+str(len(results))+' 场牛客比赛如下：'+ans+"\n\n防风控编码"+str(time.time())

async def get_prenowcoder(counts):
    results=[]
    
    #* 牛客
    # response=requests.get("https://ac.nowcoder.com/acm/contest/vip-index")
    # res=response.text
    f=open('nc.txt','r',encoding='utf-8')
    res=f.read()
    f.close()
    res = BeautifulSoup(res, "html.parser")
    res = res.select('.platform-mod.js-end .platform-item.js-item.finish')
    for ress in res:
        # 选择比赛介绍
        cont=ress.select('.platform-item-cont')[0]
        name=cont.select('h4 a')[0].text
        DateTime=cont.select('.platform-info .match-time-icon')[0].text
        st=DateTime.find("报名时间： ",0)
        last=DateTime.find("\n",0)
        DateTime=DateTime[st+7:last].strip()
        contest_id=ress.select('h4 a')[0]['href']
        time_local=datetime.datetime.strptime(DateTime,'%Y-%m-%d %H:%M')
        dt=datetime.datetime.strftime(time_local,'%Y-%m-%d %H:%M:%S')
        # 加入队列中：名称，时间，id
        results.append([name,dt,contest_id])
        if len(results) >= counts:
            break
    if len(results)==0:
        return "居然找不到，可能是：\n1. bot裂了\n2. 网站裂了\n3. 缓存裂了\n4. 地球裂了"+"\n\n防风控编码"+str(time.time())
    else:
        ans=""
        for conts in results:
            ans+="\n\n比赛名称："+conts[0]
            ans+="\n比赛时间："+conts[1]
            ans+="\n比赛链接：https://ac.nowcoder.com/acm/contest/"+conts[2]
        if len(results) < counts:
            return '缓存中牛客历史比赛不足 '+str(counts)+'场，找到历史 '+str(len(results))+' 场比赛如下：'+ans+"\n\n防风控编码"+str(time.time())
        else:
            return '找到历史 '+str(len(results))+' 场牛客比赛如下：'+ans+"\n\n防风控编码"+str(time.time())