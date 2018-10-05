# -*- coding: utf-8 -*-
# @Time    : 2018/10/5 18:36
# @Author  : Woko
# @File    : test_dot_dict

import pytest
from libs import dot_dict


@pytest.fixture(params=[dot_dict.DotDict, pytest.param(dot_dict.ObjectDict, marks=pytest.mark.object)])
def the_dict(request):
    return request.param


class TestDotDict(object):
    def test_get(self, the_dict):
        d = the_dict(a=1, b='2', c=[])
        assert d.a == 1
        assert d.b == '2'
        assert d.c == []
        with pytest.raises(AttributeError):
            assert d.d
        with pytest.raises(KeyError):
            assert d['d']

    def test_set(self, the_dict):
        d = the_dict(a=1, b=2)
        d.a = 4
        assert d['a'] == d.a

    def test_next(self, the_dict):
        d = the_dict(
            a={
                'a': {
                    'a': 1
                }
            }
        )
        assert d.a
        assert d.a['a']
        if isinstance(the_dict, dot_dict.DotDict):
            with pytest.raises(AttributeError):
                assert d.a.a
        elif isinstance(the_dict, dot_dict.ObjectDict):
            assert d.a.a
            assert d.a.a.a == 1
