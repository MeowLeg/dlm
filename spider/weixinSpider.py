# coding=utf-8

from pyquery import PyQuery as pq
import os, sqlite3, re, time, urllib2, json, random
import cookielib

class RedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        print headers
        if "Location" in headers:
            return headers["Location"]
        else:
            return ""

def getDate(s):
    if re.search(r'\:', s):
        return time.strftime("%Y-%m-%d", time.localtime())
    m = re.findall(r"(\d+)", s)
    if m:
        return time.strftime("%Y", time.localtime())+"-"+("-".join(m))
    return ""

def getCookie(url):
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    opener.addheaders = [
            ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"),
            ("Upgrade-Insecure-Requests", "1"),
            ("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36"),
            ]
    opener.open(url+str(int(time.time()*1000)))
    opener.close()

    strEle = []
    for c in cookie:
        strEle.append(c.name+"="+c.value)
    return ";".join(strEle)

def buildOpener(cur):
    cookie = None
    for r in cur.execute("select cookie from cookie order by random() limit 1"):
        cookie = r[0]
    if cookie is None: 
        raise Exception("No Cookie!")

    opener = urllib2.build_opener(urllib2.HTTPHandler(), RedirectHandler)
    opener.addheaders = [
        ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"),
        ("Upgrade-Insecure-Requests", "1"),
        ("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36"),
        ("Cookie", cookie)
        ]
    return opener

def getBodyContent(opener, url):
    # sogou.weixin.gzhcb(...)
    print url+str(int(time.time()*1000))
    body = opener.open(url+str(int(time.time()*1000))).read()
    m = re.match(r'\s*sogou.weixin.gzhcb\((.*)\).*', body)
    return m.group(1)

def getOpenid(url):
    return url.split("&")[1].split("=")[1]

def getElement(e, s):
    m = re.search('<'+e+r'><!\[CDATA\[(.*?)\]\]>', s)
    if m:
        return m.group(1)
    else:
        return ""

def getLastModified(s):
    m = re.search(r'<lastModified>(\d+)<\/lastModified>', s)
    return time.strftime("%Y-%m-%d", time.localtime(int(m.group(1))))

def formJson(data):
    j = json.loads(data)
    # print getLastModified(j["items"][0])
    return [[getElement("title", l),
        getElement("imglink", l),
        "http://weixin.sogou.com"+getElement("url", l),
        getLastModified(l)] for l in j["items"]]

def downloadImg(url, i):
    imgName = str(i)+"."+url.split("=")[1]
    # cmd = "wget "+url+" -O /home/jh/busvideo/"+imgName
    cmd = "wget "+url+" -O ./"+imgName # FIX ME
    os.system(cmd)
    return imgName

def getImg(d, db, cur):
    for i, url in d:
        try:
            cur.execute("update weixin set img = ? where id = ?", (downloadImg(url,i), i))
            db.commit()
        except Exception,e:
            print e

def getLocation(opener, url):
    return opener.open(url)

def getExt(name):
    m = re.search(r';ext=(.+?)\"', urllib2.urlopen("http://weixin.sogou.com/weixin?type=1&query="+name+"&ie=utf8").read(), re.M|re.S)
    if m: return m.group(1)

def formUrls(urls):
    return ["http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb&openid="+openid+"&ext="+getExt(name)+"&gzhArtKeyWord=&page=1&t="+str(int(time.time())) for openid, name in urls]

def log2Db(urls, db, cur):
    opener = buildOpener(cur) # NEED TO VERIFY -- VERIFIED
    downloads = []
    for u in formUrls(urls):
        if u.find("/websearch%") == 0: continue
        key = getOpenid(u)
        body = getBodyContent(opener, u)

        for r in formJson(body):
            try:
                r[-2] = getLocation(opener, r[-2]) # NEED TO VERIFY -- VERIFIED
                time.sleep(5)
                if r[-2] == "": continue
                cur.execute("insert into weixin(title, img, href, logdate, key) values(?,?,?,?,?)", r+[key])
                downloads.append([cur.lastrowid, r[1]])
            except Exception, e:
                print e
        time.sleep(int(random.random()*60)+1)
    db.commit()
    db.close()
    getImg(downloads, db, cur)

def loopSpider(urls, dbPath):
    db = sqlite3.connect(dbPath)
    cur = db.cursor()
    lastId = -1
    for r  in cur.execute("select lastId from lastSpider order by id desc limit 1"):
        lastId = r[0]
    lastId += 1
    if lastId >= len(urls):
        lastId = 0
    log2Db([urls[lastId]], db, cur)
    cur.execute("insert into lastSpider(lastId) values (?)", (lastId,))
    db.commit()

if __name__ == '__main__':
    urls = [
            ("oIWsFtzlRvsDVd2e69iSjjYcTbW8", "舟山广电"), # 舟山广电
            ("oIWsFt_90Pc5J5qYypXzgI9E11Rs", "讲拨侬听"), # 讲拨侬听
            ("oIWsFt0JFB3-dVvN7xqgLwG7lTZQ", "汪大姐来了"), # 汪大姐来了
            ("oIWsFt5bh4aAeUwAgsLrGjBke2A0", "舟山新闻综合频道"), # 舟山新闻综合频道
            ("oIWsFt1OUb1JyTvY7AVBizjd4F-w", "舟山电视公共生活频道"), # 舟山电视公共生活频道
            ("oIWsFtyXxULy9FfmEMrpYoo0Rxu4", "群岛旅游频道"), # 群岛旅游频道
            ("oIWsFt8cgf4W8lutaRBM-4jC0nEA", "新闻998"), # 新闻998
            ("oIWsFt-QtI5IGCGtE1Uc46aj0WZI", "交通97"), # 交通97
            ("oIWsFt_HcL1-Bt57PtLs3NZbAYo8", "FM91"), # FM91
            ("oIWsFt232h6j4SHUooOXzc1wcaXs", "舟山新周报") # 舟山新周报
            ]
    # log2Db(urls)
    dbPath = "/home/station6945/Code/dlm/middle.db" # FIX ME
    loopSpider(urls, dbPath)
