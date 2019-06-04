# -*- coding: utf-8 -*-
# @Time    : 2019/3/3 21:00
# @Author  : Woko
# @File    : __init__.py.py


"""
Official Website: http://sc.ftqq.com
"""

import requests


def wechat(text, desp):
    """send to wechat for one person"""
    with open('./tools/server_chan/server.key', 'r') as f:
        secret = f.read()
    secret = secret.replace('\n', '')
    requests.get('https://sc.ftqq.com/' + secret + '.send',
                 params={'text': text, 'desp': desp})


def wechat_channel(text, desp):
    """send to wechat for all person subscribed thic channel"""
    with open('./tools/server_chan/sendkey.key', 'r') as f:
        send_key = f.read()
    send_key = send_key.replace('\n', '')
    params = {
        'SendKey': send_key,
        'text': text,
        'desp': desp,
    }
    requests.get('https://pushbear.ftqq.com/sub', params=params)
