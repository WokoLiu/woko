# -*- coding: utf-8 -*-
# @Time    : 2019-06-04 17:48
# @Author  : Woko
# @File    : datetime_module.py

"""用于记录日期时间的各种格式以及转换方式
需要考虑的类型有以下几种：
1. datetime.datetime
2. timestamp (int or float)
3. format string
4. datetime.date

ps: 只写各种时间与 datetime.datetime 的互相转化
"""
import datetime
import sys
import time

PY2 = sys.version_info[0] < 3


def basic(sky: datetime.datetime):
    """基本结构可以拆除哪些信息"""
    print('\nbasic')
    print(sky)  # 完整时间
    print(sky.year)  # 年
    print(sky.month)  # 月
    print(sky.day)  # 日
    print(sky.hour)  # 时
    print(sky.minute)  # 分
    print(sky.second)  # 秒
    print(sky.date())  # 日期
    print(sky.time())  # 时间


def with_timestamp(sky: datetime.datetime):
    """基本结构与时间戳"""
    if PY2:
        sky_timestamps = time.mktime(sky.timetuple())
    else:
        sky_timestamps = sky.timestamp()

    the_sky = datetime.datetime.fromtimestamp(sky_timestamps)
    print('\nwith_timestamp')
    print(the_sky, sky_timestamps, int(sky_timestamps * 1000))


def with_string(sky: datetime.datetime):
    """基本结构与字符串"""
    sky_str = sky.strftime('%Y-%m-%d %H:%M:%S')
    if sys.version_info > (3, 7):
        # 只有 iso 标准格式的时候可以这样
        the_sky = datetime.datetime.fromisoformat(sky_str)
    else:
        the_sky = datetime.datetime.strptime(sky_str, '%Y-%m-%d %H:%M:%S')
    print('\nwith_string')
    print(the_sky, sky_str)


def with_date(sky: datetime.datetime):
    """基本结构与日期"""
    sky_date = sky.date()
    the_sky1 = datetime.datetime(sky_date.year, sky_date.month, sky_date.day)
    the_sky2 = datetime.datetime.combine(sky_date, datetime.datetime.min.time())
    print('\nwith_date')
    print(sky_date, the_sky1, the_sky2)


def get_now():
    """获取当前时间"""
    datetime_today = datetime.datetime.today()
    datetime_now = datetime.datetime.now()
    timestamp_now = time.time()
    str_now = str(datetime_now)
    print('\nnow')
    print(datetime_now, timestamp_now, str_now)


if __name__ == '__main__':
    # 一个待转换的标准时间
    sky = datetime.datetime(2008, 8, 8, 8, 8, 8)
    basic(sky)
    with_timestamp(sky)
    with_string(sky)
    with_date(sky)
    get_now()
