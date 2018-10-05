# -*- coding: utf-8 -*-
# @Time    : 2018/10/5 21:45
# @Author  : Woko
# @File    : test_bloom_filter.py

import pytest
from algorithm.bloom_filter import *


@pytest.fixture(params=[MemoryStringBitMap, MemoryStringBitMap, MemoryStringBitMap, RedisBitMap])
def bloom_filter(request):
    """make bloom_filter"""
    bit_size = 20
    map_num = 2
    bit_map = request.param(bit_size, map_num)
    func_list = build_hash_func_list(bit_size)
    return BloomFilter(bit_map, func_list, map_num)


@pytest.fixture(params=['https://github.com/WokoLiu'])
def key_list(request):
    """make filter_key list to test"""
    res = [request.param]
    for i in range(10):
        res.append(request.param + str(i))
    return res


class TestBloomFilter(object):
    def test_bloom_filter(self, bloom_filter, key_list):
        for key in key_list:
            assert not bloom_filter.is_contain(key)
            bloom_filter.insert(key)
            assert bloom_filter.is_contain(key)
