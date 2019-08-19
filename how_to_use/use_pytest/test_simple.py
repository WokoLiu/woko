# -*- coding: utf-8 -*-
# @Time    : 2018/10/4 10:14
# @Author  : Woko
# @File    : test_simple.py

import warnings
import pytest


def inc(x):
    return x + 1


def will_raise():
    raise KeyError('lalala')


def test_inc():
    warnings.warn(UserWarning('test_inc must be rewrite'))
    assert inc(3) == 4


@pytest.mark.lalala
def test_will_raise():
    with pytest.raises(KeyError):
        will_raise()


@pytest.mark.usefixtures('just_fixture')
@pytest.mark.usefixtures('just_session')
class TestSimple(object):
    def test_one(self):
        x = "this"
        assert 'h' in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, 'check')


# content of test_tmpdir.py
def test_needsfiles(tmpdir):
    print(tmpdir)
    assert 1


# test conftest.py
def test_old_dict(old_dict):
    assert old_dict['a'] == 1
    old_dict['b'] = 3


@pytest.mark.usefixtures('just_session')
def test_old_dict2(old_dict):
    print(old_dict)
    assert old_dict['b'] == 3


if __name__ == '__main__':
    pytest.main()