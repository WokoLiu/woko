# -*- coding: utf-8 -*-
# @Time    : 2019/3/3 21:00
# @Author  : Woko
# @File    : __init__.py.py


"""
Official Website: http://sc.ftqq.com
"""

import requests


def wechat(text, desp):
    with open('server.key', 'r') as f:
        secret = f.read()
    secret = secret.replace('\n', '')
    requests.get('https://sc.ftqq.com/' + secret + '.send', params={'text': text, 'desp': desp})
