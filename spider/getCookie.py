# coding=utf-8

import urllib2
import cookielib
import sqlite3
import time

def getSougouWeixinSearchCookie(url):
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    opener.addheaders = [
            ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"),
            ("Upgrade-Insecure-Requests", "1"),
            ("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36"),
            ]

    opener.open(url+str(int(time.time()*1000))).read()
    opener.close()

    strEle = []
    for c in cookie:
        strEle.append(c.name+"="+c.value)

    return ";".join(strEle)

def logIntoDb(cookie, dbPath):
    print cookie
    db = sqlite3.connect(dbPath)
    cur = db.cursor()
    cur.execute("delete from cookie")
    cur.execute("insert into cookie(cookie) values(?)", (cookie,))
    db.commit()

if __name__ == "__main__":
    url = "http://weixin.sogou.com/gzh?openid=oIWsFtzlRvsDVd2e69iSjjYcTbW8&ext=h3pzFjLZCZ0p2TwsGA-6Xxg0W3CMAFfeb_Cr4UDNmsW256Cvw6mL9CrC2-GkDaCn" # 舟山广电
    dbPath = "/home/station6945/Code/dlm/middle.db" # FIX ME
    logIntoDb(getSougouWeixinSearchCookie(url), dbPath)
