# -*- coding: utf-8 -*-
# @Time    : 2018/7/27 14:25
# @Author  : Woko
# @File    : bloom_filter.py

"""布隆过滤器，用于检测一个值是否在一个集合里
整体分三部分：1. 过滤器本体，2. 存储集合的工具，3. 一组哈希函数
参考文档：
公式指导：https://blog.csdn.net/qq_18495465/article/details/78500472
python实现及redis.bitmap大小的选择：https://blog.csdn.net/Bone_ACE/article/details/53107018
"""

from hashlib import md5
from build_hash import BitHash


class BitMap(object):
    """布隆过滤器使用的存储集合"""
    def __init__(self, bit_size, **kwargs):
        """
        :param bit_size: 总比特位数
        """
        self.bit = bit_size
        self.cap = 1 << bit_size  # bit map 总大小
        self.__conf = kwargs

    def __getattr__(self, item):
        return self.__conf[item]

    def get_bit(self, value):
        """获取比特位的值"""
        raise NotImplementedError

    def set_bit(self, value):
        """设置比特位的值"""
        raise NotImplementedError


class MemoryListBitMap(BitMap):
    """在内存里，使用list来存储
    会占据超大量内存，无法处理超大量的数据（放在这里只是展示一下功能，实际上肯定不会使用这个）
    """
    def __init__(self, bit_size):
        super(MemoryListBitMap, self).__init__(bit_size)
        self.map = [0] * self.cap  # 1, 0, True, False，所占空间都是24byte

    def get_bit(self, value):
        if not value:
            return 0
        if self.map[value]:
            return 1
        else:
            return 0

    def set_bit(self, value):
        self.map[value] = 1


class BloomFilter(object):
    """布隆过滤器本体"""
    def __init__(self, bit_map, hash_func):
        """
        :param bit_map: 数据集合
        :param hash_func: 哈希函数组
        """
        self.bit_map = bit_map
        self.hash_func = hash_func

    def is_contain(self, value):
        """检测value是否在集合里"""
        if not value:
            return False
        value = md5(value).hexdigest()
        res = True
        for f in self.hash_func:
            loc = f.hash_str(value)
            res = res & self.bit_map.get_bit(loc)
        return res

    def insert(self, value):
        """将这个值插入集合"""
        value = md5(value).hexdigest()
        for f in self.hash_func:
            loc = f.hash_str(value)
            self.bit_map.set_bit(loc)


def build_hash_func_list(bit, key=7):
    """构建哈希函数组"""
    seeds = [5, 7, 11, 13, 31, 37, 61, 103, 151, 173]  # 都是质数，但选择规则我还不清楚
    func_list = []
    for seed in seeds[:key]:
        func_list.append(BitHash(bit, seed))
    return func_list


def test_one(bf, test_key):
    """测试一个值有没有在集合里"""
    if bf.is_contain(test_key):
        print 'yes', test_key
    else:
        print 'no', test_key
        bf.insert(test_key)


def run():
    bit_size = 8
    test_key = 'https://github.com/WokoLiu'
    bit_map = MemoryListBitMap(bit_size)
    func_list = build_hash_func_list(bit_size)
    bf = BloomFilter(bit_map, func_list)

    test_one(bf, test_key)
    test_one(bf, test_key)
    test_one(bf, test_key+'1')
    test_one(bf, test_key+'1')

if __name__ == '__main__':
    run()
