# -*- coding: utf-8 -*-
# @Time    : 2017/6/5 18:13
# @Author  : Woko
# @File    : dot_dict.py


class DotDict(dict):
    """
    使用点操作符访问dict
    """
    def __init__(self, *args, **kwargs):
        super(DotDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


if __name__ == '__main__':
    old = {
        'a': 1,
        'b': 2,
        'c': 3,
    }
    try:
        print old.__dict__
    except AttributeError as e:
        print e.message
        print 'dict类没有__dict__属性，惊不惊喜~意不意外~'
    new = DotDict(old)
    print new, type(new)
    print new.__dict__
    print new.a
    print new.b
    print new.c

    xx = DotDict(f=4, y=5)
    print xx.f
