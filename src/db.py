#coding=utf-8

import urllib
import urllib2
import cookielib
import re
import json
import requests


class DB(object):
    def __init__(self, email, passwd):
        self.url = "http://www.douban.com/accounts/login"
        self.post = {
            'form_email':email,
            'form_password':passwd,
            'source':'index_nav'
            }
        cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        self.response = self.opener.open(self.url, urllib.urlencode(self.post))

    def login(self):
        print self.response.geturl()
        if self.response.geturl() == self.url:
            print 'logining...'
            html = self.response.read()
            reg = r'<img id="captcha_image" src="(.*?)" alt="captcha" class="captcha_image"/>'
            imglist = re.findall(reg, html)
            urllib.urlretrieve(imglist[0], 'captcha.jpg')
            captcha = raw_input('captcha is: ')
            regid = r'<input type="hidden" name="captcha-id" value="(.*?)"/>'
            ids = re.findall(regid, html)
            self.post["captcha-solution"] = captcha
            self.post["captcha-id"] = ids[0]
            self.post["login"] = "登录"
            self.post["redir"] = 'http://www.douban.com'
            self.response = self.opener.open(self.url, urllib.urlencode(self.post))
            print self.response.geturl()
            if self.response.geturl() == "http://www.douban.com/":
                print 'login success !'
                print self.response.read()
        elif self.response.geturl() == "http://www.douban.com":
            print 'login success !'
            print self.response.read()
            
    
    def getMainPage(self):
        url = "http://www.douban.com"
        resp  = self.opener.open(url)
        print resp.read()  
        
    def getSidsByPageNum(self, pageNum):
        _market_api_url = "https://market.douban.com/api/home/shops?category=index&page=" + str(pageNum) + "&page_size=12"
        r = self.opener.open(_market_api_url)
        jsontext = json.load(r)
        return jsontext['data']['shops'][0]['sid']
    
    def followShop(self, shopName):
        _follow_shop_url = "https://market.douban.com/api/shops/" + shopName + "/follow"
        _follow_post_data = {'ck':"xV-v"}
        r = self.opener.open(_follow_shop_url, urllib.urlencode(_follow_post_data))
        print json.load(r)
    
    def getAllShops(self):
        shoplist = []
        for page in range(1, 12):
            _market_api_url = "https://market.douban.com/api/home/shops?category=index&page=" + str(page) + "&page_size=12"
            r = self.opener.open(_market_api_url)
            jsontext = json.load(r)
            shops = jsontext['data']['shops']
            total = jsontext['data']['total']
            for i in range(total):
                shoplist.append(shops[i]['sid'])
        return shoplist   
            
        
    def followAllShop(self):
        shops = self.getAllShops()
        for shop in shops:
            _follow_shop_url = "https://market.douban.com/api/shops/" + shop + "/follow"
            _follow_post_data = {'ck':"xV-v"}
            r = self.opener.open(_follow_shop_url, urllib.urlencode(_follow_post_data))
            result = json.load(r)
            if result['r'] == 0:
                print 'follow the shop ' + shop + ' success.'
     
def test():
    url = "https://market.douban.com/api/home/shops?category=index&page=2&page_size=12"
    r = requests.get(url)
    print r.json()
    
email = raw_input('Your email: ')
passwd = raw_input('Your passwd: ')   
my = DB(email, passwd)         
my.login()
# my.followAllShop()