#coding=utf-8

import requests
import re

_douban_login_url = "https://accounts.douban.com/login"

data = {}
data['source'] = None
data['redir'] = 'http://www.douban.com'
data['form_email'] = 'afterbe@sina.com'
data['form_password'] = 'lichen123'
data['captcha-solution'] = 'learning'
data['captcha-id'] = 'FWims5ng2Q9gBn0bmIAyeOWT:en'
data['remember'] = 'on'
data['login'] = '登录'
r = requests.post(_douban_login_url, data = data)
print r.text
print r.json
print r.cookies