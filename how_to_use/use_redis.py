# -*- coding: utf-8 -*-
# @Time    : 2018/7/24 19:18
# @Author  : Woko
# @File    : use_redis.py

"""python使用redis
参考文档：
中文官网：http://redis.cn
一个旧版本命令手册：http://doc.redisfans.com/index.html
一个python整理文档：https://blog.csdn.net/drdairen/article/details/50957602

python的redis模块提供了两个client，redis.StrictRedis是完全符合官方命令的，推荐使用
redis.Redis是StrictRedis的子集，用来向后兼容，部分方法实现不同，不推荐使用

Redis一共有14个redis命令组，两百多个redis命令，命令组如下：
Cluster、Connection、Geo、Hashes、HyperLogLog、Keys、Lists、Pub/Sub、
Scripting、Server、Sets、Sorted Sets、Strings、Transactions

先写常用命令组吧
Keys组：


"""

import datetime
import redis

server = redis.StrictRedis(host='localhost', port=6379, db=0)
server_db2 = redis.StrictRedis(host='localhost', port=6379, db=1)

key = 'test'
value = 'this is test value'
ex = 300

print('\nKeys组')
print(server.keys('*'))
print(server.delete('bloomfilter0'))
print(server.set(key, value, ex=ex))
print(server.exists(key))
print(server.expire(key, 100))
print(server.expireat(key, datetime.datetime.now()+datetime.timedelta(minutes=10)))
print(server.keys('t*'))
print(server.pttl(key))
print(server.randomkey())
print(server.rename(key, 'test22'))
print(server.renamenx('test22', key))
dumped = server.dump(key)
print(dumped)
print(server.restore('another_test', 10, dumped))
print(server.get('another_test'))
print(server.move(key, 1))
print(server_db2.keys('t*'))
print(server.keys('t*'))
