# -*- coding: utf-8 -*-
# @Time    : 2019/2/21 20:15
# @Author  : Woko
# @File    : process_monitor.py


import os

from tools.server_chan import wechat

res = os.popen('ps aux | grep lalala | wc -l').read().strip()

if res.isdigit() and int(res) > 41:
    text = 'belletone_01_warning',
    desp = 'sync_im_user process %s' % res
    wechat(text, desp)
