# -*- coding: utf-8 -*-
# @Time    : 2019/2/18 20:31
# @Author  : Woko
# @File    : file_monitor.py

import sys

if sys.version_info > (3,):
    string = str
else:
    string = unicode

from tools.server_chan import wechat


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
