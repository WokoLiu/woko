# -*- coding: utf-8 -*-
# @Time    : 2018/10/8 23:20
# @Author  : Woko
# @File    : test_build_hash.py

import random
import string
from hashlib import md5
import pytest
from algorithm import build_hash


@pytest.fixture(scope='module')
def str_values():
    res = set()
    for _ in range(100):
        res.add(''.join(random.sample(string.printable, random.randint(0, 100))))
    return res


@pytest.fixture(scope='module')
def int_values():
    return list(range(1000))


class RotateHashForTest(build_hash.Hash):
    @build_hash.RotateHash()
    def hash_int(self, value):
        return value

    @build_hash.RotateHash()
    def hash_str(self, value):
        return value


@pytest.fixture(
    params=[build_hash.DirectHash(), build_hash.ModHash(997), build_hash.SqrtMiddleHash(4),
            build_hash.FoldHash(5), build_hash.BitHash(31, 11), RotateHashForTest()],
    ids=['DirectHash', 'ModHash', 'SqrtMiddleHash', 'FoldHash', 'BitHash', 'RotateHash'])
def hash_obj(request):
    return request.param


class TestNeedMd5(object):
    @pytest.fixture
    def foo(self):
        class Foo(object):
            @build_hash.need_md5
            def with_md5(self, value):
                return value

        return Foo()

    def test_str(self, foo, str_values):
        for i in str_values:
            assert foo.with_md5(i) == md5(bytes(i, encoding='utf-8')).hexdigest()

    def test_int(self, foo, int_values):
        for i in int_values:
            assert foo.with_md5(i) == md5(str(i).encode('utf-8')).hexdigest()


class TestHash(object):
    def test_str(self, hash_obj, str_values):
        str_res = set()
        for i in str_values:
            str_res.add(hash_obj.hash_str(i))
        assert len(str_values) - len(str_res) < len(str_values) / 10

    def test_int(self, hash_obj, int_values):
        int_res = set()
        for i in int_values:
            int_res.add(hash_obj.hash_int(i))
        assert len(int_values) - len(int_res) < len(int_values) / 10
