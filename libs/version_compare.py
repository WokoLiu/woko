# -*- coding: utf-8 -*-
# @Time    : 2019-05-31 09:22
# @Author  : Yulong Liu
# @File    : version_compare.py


import re


class Version:
    def __init__(self, version: str):
        """can with channel prefix or not
        attention: 1.2.3 equals to 1.2.300
        :exception ValueError
        """
        if '_' in version:
            try:
                self.channel, self.version_num = version.split('_')
            except ValueError:
                raise ValueError('version format error')
        else:
            self.version_num = version
            self.channel = ''

        if re.match(r'^(\d|[1-9]\d)\.\d\.(\d|\d{3})$', self.version_num) is None:
            raise ValueError('version num format error')
        else:
            high, middle, low = (x for x in self.version_num.split('.'))
            self.high = int(high)
            self.middle = int(middle)
            self.low = int(low.ljust(3, '0'))
            self.compare_str = '.'.join(
                (str(self.high), str(self.middle), str(self.low)))

    def __str__(self):
        if self.channel:
            return self.channel + '_' + self.version_num
        else:
            return self.version_num

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        """support str and Version type"""
        if isinstance(other, str):
            return self < Version(other)
        if self.high != other.high:
            return self.high < other.high
        if self.middle != other.middle:
            return self.middle < other.middle
        if self.low != other.low:
            return self.low < other.low
        return False

    def __eq__(self, other):
        """support str and Version type"""
        if isinstance(other, str):
            return self == Version(other)
        return self.high == other.high \
               and self.middle == other.middle \
               and self.low == other.low

    def __gt__(self, other):
        if isinstance(other, str):
            return self > Version(other)
        if self.high != other.high:
            return self.high > other.high
        if self.middle != other.middle:
            return self.middle > other.middle
        if self.low != other.low:
            return self.low > other.low
        return False

    def __le__(self, other):
        return not self.__gt__(other)

    def __ge__(self, other):
        return not self.__lt__(other)
