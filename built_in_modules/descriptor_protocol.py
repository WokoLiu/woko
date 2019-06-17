# -*- coding: utf-8 -*-
# @Time    : 2019-06-17 12:32
# @Author  : Woko
# @File    : descriptor_protocol.py

"""描述符
是指实现了 __get__(), __set__(), __delete__() 中至少一个方法的对象
影响了 python 里对方法和属性的查找顺序

通常用来对类属性的 get/set 做处理

"""
import types
from weakref import WeakKeyDictionary


# 一、定义描述符的方式：
# 1. 用类定义
class Grade(object):
    def __init__(self):
        # WerkKeyDictionary 对描述符本身没有特殊作用，这里可以理解成 dict()
        self._values = WeakKeyDictionary()

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must between 0 and 100')
        self._values[instance] = value


# 2. 用 property 函数定义
class User(object):
    def __init__(self):
        self._email = None

    def _get_email(self):
        return self._email

    def _set_email(self, email):
        if '@' not in email:
            raise ValueError('email not valid')
        self._email = email

    def _del_email(self):
        del self._email

    # property 返回
    email = property(_get_email, _set_email, _del_email, 'this is email property')


# 第一种用法，包装类属性，但允许不同实例分别使用(假装实例属性)
# 也可以各个实例使用同一个属性
class Exam(object):
    math_grade = Grade()


first_exam = Exam()
first_exam.math_grade = 40
second_exam = Exam()
second_exam.math_grade = 80
assert first_exam.math_grade == 40
assert second_exam.math_grade == 80


# 第二种用法，包装类方法
# （装饰器也能干同样的事，但这里可以显式拿到 instance）
class Log(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, instance, owner):
        print(self.f.__name__, 'is calling')
        return types.MethodType(self.f, instance)


class C:
    @Log
    def f(self):
        pass


C().f()
