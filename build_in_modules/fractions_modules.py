# -*- coding: utf-8 -*-
# @Time    : 2018/7/8 23:16
# @Author  : Woko
# @File    : fractions_modules.py

"""
处理分数的包，所有输入的数都必须是 numbers.Rational(有理数)，但支持多种格式输入
没法直接获取带分数的整数部分

这个包里还顺便带了一个求最大公约数的方法 fractions.gcd
"""

from fractions import Fraction, gcd
from decimal import Decimal

print('初始化方式：')
print(Fraction('2e-2'))
print(Fraction('3/13'))
print(Fraction('24.5'))
print(Fraction(Decimal('1.3')))

print('\n分数计算：')
a = Fraction(3, 10)
b = Fraction(12, 11)
print(a, b)
c = a + b
print(c)
print(c.numerator, type(c.numerator))
print(c.denominator)
print(a - b)
print(a * b)
print(a / b)
print(a ** b)

# print('\n最大公约数：')
# print(gcd(864, 468))  # use math.gcd()
