# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 18:25
# @Author  : Woko
# @File    : math_modules.py

"""内置的math类，包含一些数学方法，全都是functions，基本都返回float
注：math是cmath的子集，math只提供对实数的操作，返回大多为float
    而cmath提供对复数的操作，返回大多为实部虚部均为float的复数

这里只写math，不写cmath
math参见文档：https://blog.csdn.net/u011225629/article/details/78458724

自然对数e
圆周率pi

非数字：nan，可定义nan = float('nan')
无限大：inf，可定义inf = float('inf')
判断函数：isnan(x), isinf(x)

角度和弧度转换
角度转弧度：radians(x)
弧度转角度：degrees(x)

三角函数
tan(x), sin(x), cos(x) 等等，接收的x是弧度
勾股定理：hypot(x, y)，返回以x和y为两直角边的斜边长度

取整：
向上取整：ceil(x)
向下取整：floor(x)
取整数部分：trunc(x)，这里返回的是int类型，而不是float
取整数和小数部分：modf(x)，这个会失去精度，而且这样的函数真没想到有什么用

对数&幂：
乘方：pow(x, y)，等价于 x ** y
平方根：sqrt(x)，只有平方根，n次方根可以活用pow，使用pow(x, 1.0/n)即为开x的n次方根
对数：log(x, base=e)：默认是自然对数，但基可改
常用对数：log10(x)，等价于 lambda x: math.log(x, 10)
一个特殊对数：log1p(x)，返回(1+x)的自然对数，等价于 lambda x: math.log(1+x)

阶乘：factorial(x)

内置函数的另一个版本：
绝对值：fabs(x)，不能操作复数，返回必为float
累加：fsum()，无损精度
取余：fmod(x, y)，只返回余数，等价于 x % y

其他：
copysign(x, y)：如函数名，把y的符号赋给x，然后返回x。即 lambda x, y: -1*math.fabs(x) if y < 0 else math.fabs(x)
以及一些我不认识的函数，现在不想看他们
"""

import math

pi = math.pi

print '\n三角函数'
print math.tan(0.25 * pi)
print math.sin(0.5 * pi)
print math.cos(2/3 * pi)
print math.hypot(3, 4)

print '\n弧度交互转换'
print math.radians(180) / pi
print math.degrees(pi) / 180

print '\n幂函数'
print math.pow(2, 3) - 2**3
print math.sqrt(4)
print math.pow(8, 1.0/3)
print 625 ** (1./4)

print '\n对数函数'
print math.log(math.e)
print math.log1p(math.e-1)
print math.log10(10)
log_10 = lambda x: math.log(x, 10)
print log_10(10)

print '\n阶乘'
print math.factorial(5)

print '\n内置函数的另一个版本'
print abs(-1+1j)
print math.fabs(-1.2)

nums = [1.23e+18, 1, -1.23e+18]
print sum(nums)
print math.fsum(nums)
print math.fmod(10, 3), 10 % 3

print '\n非数字和无穷大'
nan = float('nan')
inf = float('inf')
print nan, inf
print math.isnan(nan)
print math.isnan(inf)
print math.isinf(inf)
print math.isinf(1e+308)
print math.isinf(1e+309)

print '\n取整'
print math.ceil(8.8)
print math.floor(8.8)
print math.trunc(2.4), type(math.trunc(2.4))
print math.modf(3.4)

print '\n其他'
print math.copysign(-3, 1)
copysign = lambda x, y: -1*math.fabs(x) if y < 0 else math.fabs(x)
print copysign(-3, 1)
