# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 18:25
# @Author  : Woko
# @File    : math_modules.py

"""内置的math类，包含一些数学方法，全都是functions，都返回float
参见文档：https://blog.csdn.net/u011225629/article/details/78458724

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
取整数部分：trunc(x)
取整数和小数部分：modf(x)，这个会失去精度，而且这样的函数真没想到有什么用

乘方：pow(x, y)，等价于 x ** y
平方根：sqrt(x)，只有平方根，n次方根要用：
对数log(x, base=e)：默认是自然对数，但基可改
阶乘：factorial(x)

内置函数的另一个版本：
绝对值：fabs(x)，不能操作复数，返回必为float
累加：fsum()，无损精度
取余：fmod(x, y)，只返回余数，等价于 x % y
"""

import math

pi = math.pi

print math.tan(0.25 * pi)
print math.sin(0.5 * pi)
print math.cos(2/3 * pi)
print math.hypot(3, 4)

print math.radians(180) / pi
print math.degrees(pi) / 180

print math.pow(2, 3) - 2**3
print math.sqrt(4)

print math.log1p(math.e-1)
print math.log10(10)

print math.factorial(5)

print abs(-1+1j)
print math.fabs(-1.2)

nums = [1.23e+18, 1, -1.23e+18]
print sum(nums)
print math.fsum(nums)

nan = float('nan')
inf = float('inf')
print nan, inf
print math.isnan(nan)
print math.isnan(inf)
print math.isinf(inf)
print math.isinf(1e+308)
print math.isinf(1e+309)

print math.trunc(2.4), type(math.trunc(2.4))
print math.modf(3.4)
print math.fmod(10, 3), 10 % 3