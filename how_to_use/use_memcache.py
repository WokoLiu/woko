# -*- coding: utf-8 -*-
# @Time    : 2018/7/29 00:08
# @Author  : Woko
# @File    : use_memcache.py

import memcache

conn = memcache.Client(['localhost'])
print(conn)

print(conn.set('k1', 'v1'))
print(conn.get('k1'))