# -*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib


class WeiboSpider(object):
  def __init__(self):
    self.CQU_URL = 'http://weibo.cn/cqdx'
    self.CQU_LIVE_URL = 'http://weibo.cn/cqulive'
    self.WEIBO_RAND_URL = 'http://login.weibo.cn/login/?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%D0%C2%C0%CB%CE%A2%B2%A9&vt='
    self.WEIBO_LOGIN_PREFIX = 'http://login.weibo.cn/login/?'
    self.WEIBO_LOGIN_POSTFIX = '&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%D0%C2%C0%CB%CE%A2%B2%A9&vt=4&revalid=2&ns=1'
    self.cookie = cookielib.CookieJar()
    self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))


  def login(self,username,password):
    self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0'}
    request = urllib2.Request(self.WEIBO_RAND_URL, urllib.urlencode({}), self.headers)
    response = urllib2.urlopen(request)
    page = response.read()


    beginPos = page.index('rand=')
    rand = page[beginPos + 5: beginPos + 15]
    if rand.isdigit():
      pass
    else:
      rand = rand[:9]
    beginPos = page.index('''"password" name="''')
    passwordrand = page[beginPos + 17: beginPos + 30]
    beginPos = page.index('''"vk" value="''')
    vk = page[beginPos + 12: beginPos + 32]


    if len(vk) != 20 or not rand.isdigit() or len(passwordrand) != 13:
      print "Random strings from html were changed by Sina"


    postdata = urllib.urlencode({'mobile': username,
                  passwordrand: password,
                  'remember': 'on',
                  'backURL': 'http://weibo.cn/',
                  'backTitle': '新浪微博',
                  'vk': vk,
                  'submit': '登录',
                  'encoding': 'utf-8'})
    try:
      request = urllib2.Request(url = self.WEIBO_LOGIN_PREFIX + rand + self.WEIBO_LOGIN_POSTFIX,
                   data = postdata,
                   headers = self.headers)
      response = self.opener.open(request)

    except Exception as e:
      print e
   
    try:
      beginPos = str(self.cookie).index('gsid_CTandWM')
      endPos = str(self.cookie).index('for', beginPos)
    except Exception as e:
      print e
    if beginPos >= endPos:
      print "cookie was changed by sina"
    else:
      cookie_value = str(self.cookie)[beginPos: endPos]
    self.headers2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0',
            'cookie': cookie_value}
  def fetch(self, url=None):
    'Give a string of the url of you weibo homepage and return a dict'
    if url == None:
      print 'No URL Given'
    else:
      request = urllib2.Request(url=self.CQU_URL,
                   data=urllib.urlencode({}),
                   headers=self.headers2)
    try:
      response = urllib2.urlopen(request)
      data = response.read()
      return data
      if data.find(">登录<") != -1:
        return None
    except Exception as e:
      print e

weibo = WeiboSpider()
weibo.login("帐号","密码")
print weibo.fetch("http://www.weibo.cn")