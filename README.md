[原版](https://github.com/CupidsBow/koishi)，在此基础上优化了代码风格并添加了对洛谷的支持，支持在查询比赛时指定查询数量，联系方式在最下方。

# koishi

基于 [nonebot2](https://github.com/nonebot/nonebot2) 与 [gocqhttp](https://github.com/Mrs4s/go-cqhttp) 的 QQ 机器人。

# 功能

- cf/precf x 返回最近 / 之前最多 x 场次 codeforces 赛事。
- atc/preatc x 返回最近 / 之前最多 x 场次 atcoder 赛事。
- luogu/preluogu x 或 洛谷/洛谷历史 x 返回最近 / 之前最多 x 场次洛谷赛事。
- nc/prenc x 或 牛客/牛客历史 x 返回最近 / 之前最多 x 场次牛客赛事。
- today 或 今日/今日比赛/今天/今天比赛 返回当天相关赛事。
- next x 或 最近/最近比赛 返回最近的下x场次赛事。
- update 手动更新数据，信息存在本地。
- help 返回指令。
- 早上 8 点 1 分自动在每个群播报当天相关赛事（直接拉进群就可以了）。
- 每个整点 30 分更新本地数据，成功发送消息 '定时更新成功' 。（嫌太频繁可以手动改一下 schedule 插件里的时间）
- 自动同意好友和拉群。

# 如何使用

安装 requirement.txt 中的插件。`pip install -r requirement.txt`

bot 文件夹是 bot 主体，下载完和 gocqhttp 一起用就行，具体如何搭建 bot 可以查看官方文档 [nonebot2](https://nonebot.dev/)。安装完脚手架后通过脚手架安装OneBotV11适配器和fastapi驱动器，之后直接 `nb run` 启动即可。

.env.dev 文件加超管，不加也没事。

schedule 插件添加「更新数据」的消息接收方。(./bot/src/plugins/schedule/\_\_init\_\_.py)(line 32)

# 特别感谢

- [nonebot2](https://github.com/nonebot/nonebot2)
- [gocqhttp](https://github.com/Mrs4s/go-cqhttp)
- [BruceKZ](https://github.com/BruceKZ)
- [CupidsBow](https://github.com/CupidsBow)

# 题外话

~~因为自己比较懒~~因为自己号经常风控， bot 挂不了在服务器上所以发在这里，不确定有没有人需要。\
最多返回 3 场次是感觉这样不至于太刷屏(¿)。\
牛客其实只爬了「牛客系列赛」界面的比赛，没有爬「高校校赛」界面的，可能闲了会加上。\
屎山代码轻喷。\
联系 QQ: 2561116362。\
代码有错误或者代码里有信息没删干净欢迎联系。
