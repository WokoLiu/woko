# -*- coding: utf-8 -*-
# @Time    : 2018/7/8 22:54
# @Author  : Woko
# @File    : decimal_number.py

"""
as you can see, 4.2 + 2.1 != 6.3
so do not calculate float number directly
use decimal
"""

from decimal import Decimal

a = 4.2
b = 2.1
print(a+b)
assert a+b != 6.3
assert a+b != Decimal('6.3')

aa = Decimal('4.2')
bb = Decimal('2.1')
print(aa+bb)
assert aa+bb != 6.3
assert aa+bb == Decimal('6.3')
