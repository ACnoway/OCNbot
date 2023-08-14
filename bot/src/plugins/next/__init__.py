from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, Message, GroupMessageEvent,MessageEvent,PrivateMessageEvent
from nonebot.params import CommandArg
import time
import json
from bs4 import BeautifulSoup
import datetime

next=on_command('next', priority=1, aliases={'最近','最近比赛'}, force_whitespace=False)

@next.handle()
async def send_receive(bot: Bot, event: MessageEvent):
    try:
        counts = int(str(event.get_message()).split()[1])
    except:
        counts = 1
    res=await get_next(counts)
    await next.finish(res)

async def get_next(counts):
    time_today=datetime.date.today()
    time_today=datetime.datetime.strftime(time_today,'%Y-%m-%d')
    today=0
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
        results.append([3,name,dt,contest_id])
    # if cnt_nowcoder!=0 and int(today)!=int(time_now): cnt_nowcoder=0
    
    n=len(results)
    if n==0: return '最近没有比赛哦'
    else:
        # contest_list.sort(key=operator.attrgetter('time'))
        ans=""
        cnt=0
        while cnt < counts and len(results) > 0:
            mintime=datetime.datetime.strptime('2099-12-12 19:00:00','%Y-%m-%d %H:%M:%S')
            # 统计最近的比赛的时间
            for conts in results:
                Tnow=datetime.datetime.strptime(conts[2],'%Y-%m-%d %H:%M:%S')
                if Tnow.__le__(mintime):
                    mintime=Tnow
            # 找到等于这个时间的比赛
            for conts in results:
                Tnow=datetime.datetime.strptime(conts[2],'%Y-%m-%d %H:%M:%S')
                if(Tnow.__eq__(mintime)):
                    ans+="\n\n比赛平台："+ojs[conts[0]][0]
                    ans+="\n比赛名称："+conts[1]
                    ans+="\n比赛时间："+conts[2]
                    ans+="\n比赛链接："+ojs[conts[0]][1]+conts[3]
                    cnt+=1
                    results.remove(conts)
                    if cnt == counts:
                        break
        if cnt < counts:
            return '最近比赛不足 '+str(counts)+'场，找到最近的 '+str(cnt)+' 场比赛如下：'+ans
        else:
            return '找到最近的 '+str(cnt)+' 场比赛如下：'+ans