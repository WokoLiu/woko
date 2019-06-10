# -*- coding: utf-8 -*-
# @Time    : 2019-06-10 10:50
# @Author  : Woko
# @File    : abc_module.py

"""abc: Abstract Base Class 抽象基类
类似于 Java 的 interface
可以提供一系列的 abstract method，由具体的子类去实现
但 register 机制让具体子类可以不必实现所有的 abstract method

另外，Java 的 interface 还有点 mixin 的意思
"""

import math
from abc import ABCMeta, abstractmethod

import six


class Drawable(six.with_metaclass(ABCMeta)):
    """一个抽象基类，包含一些抽象的方法和变量
    当然也可以包含不抽象的方法，但是这样是不是不太好？
    """

    @property
    @abstractmethod
    def size(self):
        """size of the shape"""

    @abstractmethod
    def draw(self, scale=1):
        """draw the shape with `scale` times big"""

    def double_draw(self):
        return self.draw(2)


class Circle(Drawable):
    """直接继承，作为子类
    此时必须实现抽象基类的所有 @abstractmethod 方法
    否则不允许实例化
    """

    def __init__(self, radius):
        self.radius = radius

    def draw(self, scale=1):
        return 'Drawing: a circle with radius %f'\
               % (self.radius * scale)

    @property
    def size(self):
        return self.radius ** 2 * math.pi


c = Circle(3)
print('Circle.size:', c.size)
print(c.draw())
print(c.double_draw())
assert isinstance(c, Drawable)
assert issubclass(Circle, Drawable)


class Rectangle(object):
    """使用 register，作为虚拟子类
    只影响 isinstance 和 issubclass
    没有任何其他效果（是否真的实现了抽象基类的方法，全靠自觉）
    """

    def __init__(self, length, width):
        self.length = length
        self.width = width

    @property
    def size(self):
        return self.length * self.width


# 这种 register 的方式，做插件好像很方便
Drawable.register(Rectangle)

r = Rectangle(3, 4)
print('Rectangle.size', r.size)
try:
    r.draw()
except AttributeError as e:
    print('Error:', e)

assert isinstance(r, Drawable)
assert issubclass(Rectangle, Drawable)
