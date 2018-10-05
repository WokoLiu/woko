# -*- coding: utf-8 -*-
# @Time    : 2018/10/5 20:19
# @Author  : Woko
# @File    : test_ordered_default_dict.py

import pytest
import string
from libs.ordered_default_dict import OrderedDefaultDict


@pytest.fixture(params=[int, str, list, dict, tuple])
def ordered_default_dict(request):
    return OrderedDefaultDict(request.param)


class TestOrderedDefaultDict(object):

    def test_order(self):
        # after python 3.6 dict keeps insertion order
        d = OrderedDefaultDict()
        for index, value in enumerate(string.ascii_lowercase):
            d[value] = index

        index_check = 0
        for v in d.values():
            assert v == index_check
            index_check += 1

    def test_order_with_int_key(self):
        # after python 3.6 dict keeps insertion order
        d = OrderedDefaultDict()
        for index, value in enumerate(string.ascii_lowercase):
            d[index] = value

        index_check = 0
        for k in d.keys():
            assert k == index_check
            index_check += 1

    def test_default_type(self, ordered_default_dict):
        d = ordered_default_dict
        for i in string.ascii_lowercase:
            assert isinstance(d[i], d.default_factory)

    def test_default_int(self):
        d = OrderedDefaultDict(int)
        for i in string.ascii_lowercase:
            d[i] += 1

        for v in d.values():
            assert v == 1

    def test_default_list(self):
        d = OrderedDefaultDict(list)
        for i in string.ascii_lowercase:
            d[i].append(1)

        for v in d.values():
            assert v[0] == 1
