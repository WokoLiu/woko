# -*- coding: utf-8 -*-
# @Time    : 2017/6/5 18:13
# @Author  : Woko
# @File    : dot_dict.py

"""
使用点操作符，像访问属性一样访问dict的值
当前有两种实现：
1. DocDict，比较简单粗暴，因为dict没有__dict__属性，就把self直接赋给self.__dict__，但是pylint会报E1101
2. ObjectDict，使用__getattr__为点操作符兜底，并且可以连续使用点操作符
"""

__all__ = ['DotDict', 'ObjectDict']


class DotDict(dict):
    """
    使用点操作符访问dict，但不能连续使用点操作符
    """
    # TODO 无法连续使用点操作符
    def __init__(self, *args, **kwargs):
        super(DotDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class ObjectDict(dict):
    """可以连续使用点操作符"""
    def __getattr__(self, name):
        try:
            value = self[name]
        except KeyError:
            raise AttributeError(name)
        # 下面两行可以保证连续点操作符的使用
        if isinstance(value, dict):
            value = ObjectDict(value)
        return value

    def __setattr__(self, key, value):
        self[key] = value


class Namespace(dict):
    """从这里看来的，类如其名：
    https://github.com/flask-restful/flask-restful/blob/master/flask_restful/reqparse.py#L12
    """
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, key, value):
        self[key] = value
