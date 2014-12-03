__author__ = 'Administrator'
# coding=utf-8
import requests
import re
import os
import sys
import logging
reload(sys)
sys.setdefaultencoding("utf-8")

def get_html(wordpress_url):

	# 构造requests header, 照抄就行
	s = requests.session()
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:27.0) Gecko/20100101 Firefox/27.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept': 'Language: zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
		'Accept': 'Encoding: gzip, deflate',
	}
	# 要提交的数据
	postdata = {
		'log': 'userid',
		'pwd': 'password',
		'wp-submit': '登录',
		'redirect_to': wordpress_url+'/wp-admin',
		'testcookie': '1'
	}

	# 登录页面地址
	url = wordpress_url + '/wp-login.php'

	# 请求页面
	r = s.get(url, headers=headers,timeout=5)

	# 保存cookies , 因为post数据时要将cookie传回
	cookies = dict(r.cookies)
	# print cookies
	# 登录, 提交数据
	r = s.post(url, headers=headers, cookies=cookies, data=postdata,timeout=5)

	cookies = dict(r.cookies)

	r = s.get(wordpress_url, headers=headers,cookies=cookies,timeout=5)

	return r.text
