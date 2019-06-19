# -*- coding: utf-8 -*-
# @Time    : 2019-06-19 15:31
# @Author  : Woko
# @File    : use_redis_with_pickle.py

"""在redis里使用 pickle 包，可以存储任意 python 对象
风险：
1. 若 redis 里的数据遭到修改，pickle 可能会出问题
    -> 信任的程序才用 pickle，不信任的话去用 json
2. 若存入数据后，这个类做了修改（增删属性，改名，移动位置等），反序列化会有问题
    -> 用 copyreg 库做辅助：添加默认属性，版本管理，提供引入路径等
"""

import pickle

from redis import StrictRedis


class MyRedis(object):
    def __init__(self, host='localhost', port=6379, db=0, password=''):
        self._redis_client = StrictRedis(
            host=host, port=port, db=db, password=password)

    def set(self, key, value, expire=None):
        self._redis_client.set(key, pickle.dumps(value), expire)

    def get(self, key):
        data = self._redis_client.get(key)
        if data is None:
            return None
        else:
            return pickle.loads(data)


class User(object):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return '<User: name=%s>' % self.name


redis = MyRedis()
redis.set('a', '100', 10)
assert redis.get('a') == '100'

user = User('Woko')
redis.set('user', user, 10)
another_user = redis.get('user')
print(another_user)
assert another_user == user
assert another_user is not user
