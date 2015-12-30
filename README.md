![新蓝广科](http://develop.zsgd.com:8081/markdown/img/zsgd.jpg)

##微信大联盟爬虫

---

###来由
舟山广电现有微信公众号接近10个，很难做到统一推广。借助全台统一平台——无限舟山，打造公众号融合平台，进一步扩大广电媒体影响力。

###框架结构
对搜狗微信搜索，采用爬虫+cron的架构：由于搜狗微信反爬虫很凶，所以不能一次性爬太多的数据。这里有两个cron任务：

    1. 更新cookie：由于搜狗会根据不同的有效时限cookie返回加密的302跳转连接，因此这里每天更新一次。
    2. 每小时爬一个微信号：对10个微信号循环进行爬取。
    
###配置说明

    1. 先使用gen.sql构建sqlite3数据库
    2. 在config.py中weixins列表参数。每行项内包含两个参数，一是唯一号（可任意取），二是搜狗可（唯一）搜索到的关键词。
    3. 在config.py中修改getCookie.py和weixinSpider.py中的数据库dbPath路径。
    4. 在config.py中修改weixinSpider.py中downloadImg中的图片下载路径。
    5. crontab-e，添加两个执行getCookie.py与weixinSpider.py的任务。
    
###后续
可根据[go-template](https://github.com/MeowLeg/go-template)开发应用。（本项目已经集成）
    
###开发承建
[新蓝广科](http://www.xinlantech.com)
