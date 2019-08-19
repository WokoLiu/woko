# -*- coding: utf-8 -*-
# @Time    : 2019-07-25 22:39
# @Author  : Woko
# @File    : progress_bar.py

"""进度条"""

import time


def progress_bar(num, total):
    rate = float(num) / total
    ratenum = int(100 * rate)

    r = f'\r[{"*" * ratenum}{" " * (100 - ratenum)}]{ratenum}%'
    print(r, end='\r')


for i in range(100):
    time.sleep(0.1)
    progress_bar(i + 1, 100)
