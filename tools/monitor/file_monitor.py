# -*- coding: utf-8 -*-
# @Time    : 2019/2/18 20:31
# @Author  : Woko
# @File    : file_monitor.py

import sys

import requests

if sys.version_info > (3,):
    string = str
else:
    string = unicode


def wechat(text, desp):
    with open('server.key', 'r') as f:
        secret = f.read()
    secret = secret.replace('\n', '')
    requests.get('https://sc.ftqq.com/' + secret + '.send', params={'text': text, 'desp': desp})


def run():
    filename = '__init__.py'

    with open(filename, 'rb') as f:
        f.seek(-100, 2)  # only b mode can seek(p, 2)
        data = f.read()
        if b'test' in data:
            text = 'server maybe error'
            desp = string(data, 'utf8')
            wechat(text, desp)


if __name__ == '__main__':
    run()
