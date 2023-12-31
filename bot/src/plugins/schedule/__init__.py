# 自动定时更新以及每日播报

from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, Message, GroupMessageEvent,MessageEvent,PrivateMessageEvent
from nonebot.params import CommandArg
from nonebot import require
import nonebot
import time
import json
import datetime
import requests
from bs4 import BeautifulSoup

require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

# auto_update
@scheduler.scheduled_job("cron", hour='*',minute='30',id="auto_update")
async def auto_update():
    bot=nonebot.get_bot()
    await get_luogu()
    await get_cf()
    await get_atc()
    await get_nowcoder()
    await bot.send_msg(message_type="private",message="定时更新成功"+"\n\n防风控编码"+str(time.time()),user_id=)

async def get_luogu():
    # 这里调用洛谷api，缓存进文件
    response=requests.get("https://www.luogu.com.cn/contest/list?_contentOnly=any",timeout=10,headers=headers)
    res=response.text
    pos=res.find("\"code\":200")
    if pos==-1: return
    f=open('luogu.txt','w',encoding='utf-8')
    f.write(res)
    f.close()

async def get_cf():
    # 这里调用cf api，缓存进文件
    response=requests.get("https://codeforces.com/api/contest.list?gym=false",timeout=10,headers=headers)
    res=response.text
    pos=res.find("unavailable")
    if pos!=-1: return
    res=json.dumps(response.json())
    f=open('cf.txt','w')
    f.write(res)
    f.close()

async def get_atc():
    # 这里直接爬取atcoder的比赛界面缓存进文件
    response=requests.get("https://atcoder.jp/contests/",timeout=10,headers=headers)
    res=response.text
    f=open('atc.txt','w',encoding='utf-8')
    f.write(res)
    f.close()

async def get_nowcoder():
    # 这里直接爬取牛客的比赛界面缓存进文件
    response=requests.get("https://ac.nowcoder.com/acm/contest/vip-index",timeout=10,headers=headers)
    res=response.text
    f=open('nc.txt','w',encoding='utf-8')
    f.write(res)
    f.close()

# auto_today
@scheduler.scheduled_job("cron", hour='8',minute='1',id="auto_today")
async def auto_today():
    bot=nonebot.get_bot()
    group_list=await bot.get_group_list()
    res=await get_today()
    for group in group_list:
        await bot.send_msg(
            message_type="group",
            group_id=group['group_id'],
            message=res
        )

async def get_today():
    time_today=datetime.date.today()
    time_today=datetime.datetime.strftime(time_today,'%Y-%m-%d')
    #* 存储oj的名称及网站
    ojs=[["洛谷","https://www.luogu.com.cn/contest/"],["codeforces","https://codeforces.com/contest/"],["atcoder","https://atcoder.jp"],["牛客","https://ac.nowcoder.com/acm/contest/"]]
    results=[]
    
    #* 洛谷
    # 这里简单返回一个字符串
    # 实际应用中，这里应该调用返回 luogu 的 API
    # response=requests.get("https://codeforces.com/api/contest.list?gym=false")
    # res=json.dumps(response.json())
    f = open('luogu.txt', 'r',encoding='utf-8')
    res = f.read()
    f.close()
    st = len(results)
    res = json.loads(res)['currentData']['contests']['result']
    for ress in res:
        if ress['endTime'] < time.time():
            break
        name=ress['name']
        DateTime=ress['startTime']
        contest_id=ress['id']
        time_local=time.localtime(DateTime)
        dt=time.strftime("%Y-%m-%d %H:%M:%S",time_local)
        tdtime=time.strftime("%Y-%m-%d",time_local)
        # 加入队列中：网站，名称，时间，id
        if tdtime==time_today:
            results.insert(st,[0,name,dt,str(contest_id)])
    
    #* cf
    # response=requests.get("https://codeforces.com/api/contest.list?gym=false")
    # res=json.dumps(response.json())
    f=open('cf.txt','r',encoding='utf-8')
    res=f.read()
    f.close()
    st = len(results)
    res = json.loads(res)['result']
    for ress in res:
        if ress["phase"] == "FINISHED":
            break
        name=ress['name']
        DateTime=ress['startTimeSeconds']
        contest_id=ress['id']
        time_local=time.localtime(DateTime)
        dt=time.strftime("%Y-%m-%d %H:%M:%S",time_local)
        tdtime=time.strftime("%Y-%m-%d",time_local)
        # 加入队列中：网站，名称，时间，id
        if tdtime==time_today:
            results.insert(st,[1,name,dt,str(contest_id)])
    # if cnt_cf!=0 and int(today)!=int(time_now): cnt_cf=0
    
    #* atcoder
    # response=requests.get("https://atcoder.jp/contests/")
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
        tdtime=datetime.datetime.strftime(time_local,'%Y-%m-%d')
        # 加入队列中：网站，名称，时间，id
        if tdtime==time_today:
            results.append([2,name,dt,contest_id])
    # if cnt_atc!=0 and int(today)!=int(time_now): cnt_atc=0
    
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
        tdtime=datetime.datetime.strftime(time_local,'%Y-%m-%d')
        # 加入队列中：网站，名称，时间，id
        if tdtime==time_today:
            results.append([3,name,dt,contest_id])
    # if cnt_nowcoder!=0 and int(today)!=int(time_now): cnt_nowcoder=0
    
    #* 统计答案
    ans=""
    if len(results)==0:
        return '今天没有比赛哦 =￣ω￣='+"\n\n防风控编码"+str(time.time())
    else:
        for conts in results:
            ans+="\n\n比赛平台："+ojs[conts[0]][0]
            ans+="\n比赛名称："+conts[1]
            ans+="\n比赛时间："+conts[2]
            ans+="\n比赛链接："+ojs[conts[0]][1]+conts[3]
        return '找到今天的比赛如下：'+ans+"\n\n防风控编码"+str(time.time())
