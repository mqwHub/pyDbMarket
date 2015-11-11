#coding=utf-8

import requests
import re

_market_main_url = "https://market.douban.com"
_market_api_url = "https://market.douban.com/api/home/shops?category=index&page=2&page_size=12"

def test():
    r = requests.get(_market_api_url)
    jsontext = r.json()
    shops = jsontext['data']['shops']
    shop = shops[0]
    index = shop['index']
    product = shop['skus'][0]
    _item_url = product['url']
    _object_detail_url = _market_main_url + _item_url + '?r=6' +'&index=' + str(index) + '&p=items_1&category=index'
    print _object_detail_url

class dbanSpiderException(Exception):
    def __init__(self, msg):
        Exception.__init__ (self, msg)
        self.msg = msg

def printHeader(num, charater, header):
    s = ''
    for i in range(0, 2 * num):
        if i == num:
            s = s + header + charater
        else:
            s = s + charater
    print s

def main():
    r = requests.get(_market_main_url)
    if r.status_code == 200:
        text = r.text
    else:
        raise dbanSpiderException('can not acccess...')
    # print text
    printHeader(20, '=', '秒杀商品')
    items = re.findall(r'\s{2,}title="(.+)" target="_blank">', text)
    for item in items:
        print item
    printHeader(20, '=', '店铺推荐商品')
    items = re.findall(r'<a class="title" href="/item.+">\s+<b>(.+)</b>', text)
    for item in items:
        print item
    
test()
