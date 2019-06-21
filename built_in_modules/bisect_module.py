# -*- coding: utf-8 -*-
# @Time    : 2019-06-21 10:14
# @Author  : Woko
# @File    : bisect_module.py

"""这是一个用于二分查找的库
一共包含四个函数：
bisect_right: 如果要把一个元素插入到一个有序序列里，返回应该插入到的位置。若此元素在列表中已存在，则返回其右侧的位置
bisect_left: 同上，左侧
insort_right: 比上面多一句插入，无返回值
insort_left: 同上，左侧

注1：要使用这四个函数的序列，必须是 typing.Sequence 类型，节点必须至少实现了 __lt__ 函数

注2：使用 insort 函数插入的话，序列需要实现 insert 函数
若未实现此函数，则可以用 bisect 函数找到位置，然后再手动插入
"""

import bisect


class Node(object):
    """专门用于演示的一个节点类
    把 用于查找和比较的值 和 用于输出展示的值 区分开
    以便于区分插入位置
    """

    def __init__(self, value, tag):
        """
        :param value: 用来查找和比较的
        :param tag: 用来展示节点插入位置的
        """
        self.value = value
        self.tag = tag

    def __lt__(self, other):
        if isinstance(other, Node):
            return self.value < other.value
        return self.value < other

    def __repr__(self):
        return '<%r>' % self.tag


# 原始序列
arr = [Node(x, x) for x in range(10)]
print(arr)  # [<0>, <1>, <2>, <3>, <4>, <5>, <6>, <7>, <8>, <9>]

# 插入到右侧
bisect.insort_right(arr, Node(3, 'new_to_right'))
print(arr)  # [<0>, <1>, <2>, <3>, <'new_to_right'>, <4>, <5>, <6>, <7>, <8>, <9>]

# 插入到左侧
bisect.insort_left(arr, Node(3, 'new_to_left'))
print(arr)  # [<0>, <1>, <2>, <'new_to_left'>, <3>, <'new_to_right'>, <4>, <5>, <6>, <7>, <8>, <9>]

# 如果要插入到右侧，应该插到哪个位置
assert bisect.bisect_right(arr, Node(3, 'won\'t be insert')) == 6
# 如果要插入到左侧，应该插到哪个位置
assert bisect.bisect_left(arr, Node(3, 'won\'t be insert')) == 3

# 只要是序列就可以用这个函数哇
assert bisect.bisect_right('abcde', 'c') == 3
