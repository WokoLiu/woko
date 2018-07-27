# -*- coding: utf-8 -*-
# @Time    : 2018/7/26 11:15
# @Author  : Woko
# @File    : bit_operation.py

"""python内置的位运算
参考文档：http://www.runoob.com/python/python-operators.html
&：按位与，都为1则为1
|：按位或，只要有一个为1就为1
^：按位异或，不相同时为1
~：按位取反，使用补码运算，不是单纯加个负号

位移，python的位移好像有问题，待验证，参见：https://www.cnblogs.com/zhengyun_ustc/archive/2009/10/14/shifting.html
<<：左移，高位舍弃，低位补0，小于2**32时相当于扩大2n倍
>>：右移，低位舍弃，高位补0
"""
import timeit


a = 9
b = 12
print bin(a)
print bin(b)

print bin(a & b)
print bin(a | b)
print bin(a ^ b)
print bin(~a), ~a
print bin(~b), ~b

print bin(a << 2), a << 2
print bin(b >> 2), b >> 2

x = 2 ** 32
print bin(x), x, type(x)

y = 1 << 32
print x - y

func = lambda: 2 ** 32
fund = lambda: 1 << 32
print timeit.timeit(func, number=1000000) - timeit.timeit(fund, number=1000000)
