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

import redis
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
        if not 0 <= value < self.cap:
            return 0
        return 1 if self.map[value] else 0

    def set_bit(self, value):
        self.map[value] = 1


class MemoryStringBitMap(BitMap):
    """在内存里，使用string来存储
    会占据大量内存（大概是list的1/8）
    缺点是set_bit操作非常麻烦
    """
    def __init__(self, bit_size):
        super(MemoryStringBitMap, self).__init__(bit_size)
        self.map = '0' * self.cap

    def get_bit(self, value):
        if not 0 <= value < self.cap:
            return 0
        return 1 if self.map[value] == '1' else 0

    def set_bit(self, value):
        if not 0 <= value < self.cap:
            return None
        self.map = self.map[:value] + '1' + self.map[value+1:]


class MemoryIntBitMap(BitMap):
    """在内存里，使用int来存储
    占用空间是string的 1/7.5，是list的 1/60（bit_size越大，越接近这个数字）
    速度也要快很多，但超大数量下还是会慢
    还不清楚是位移慢还是与或慢
    """
    def __init__(self, bit_size):
        super(MemoryIntBitMap, self).__init__(bit_size)
        self.map = 1 << self.cap  # 是self.cap个二进制位的一个数

    def get_bit(self, value):
        """想到了三种方式，从上到下效率依次降低"""
        if not 0 <= value < self.cap:
            return 0
        return 1 if self.map & (1 << (value-1)) else 0  # 直接判断这一位是不是有值
        # return (self.map >> (value-1)) & 1  # 先右移，再与最末位与
        # return (self.map >> (value-1)) % 2  # 先右移，再判奇偶

    def set_bit(self, value):
        """直接按位或"""
        if not 0 <= value < self.cap:
            return None
        self.map |= (1 << (value-1))


class RedisBitMap(BitMap):
    """使用redis自带的bitmap
    超级快！
    """
    def __init__(self, bit_size, host='localhost', port=6379, db=0,
                 password=None, key='bloomfilter'):
        super(RedisBitMap, self).__init__(bit_size, key=key)
        self.redis = redis.StrictRedis(host=host, port=port, db=db, password=password)

    def get_bit(self, value):
        return self.redis.getbit(self.key, value)

    def set_bit(self, value):
        self.redis.setbit(self.key, value, 1)


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


def cal_space():
    """计算空间大小"""
    import sys
    size = 1 << 30
    a = 1 << size
    b = '0' * size
    c = [0] * size
    aa = sys.getsizeof(a)
    bb = sys.getsizeof(b)
    cc = sys.getsizeof(c)
    print aa  # 143165604
    print bb  # 1073741861
    print cc  # 8589934664
    print cc / float(bb)  # 7.99999979138
    print cc / float(aa)  # 59.9999889918
    print bb / float(aa)  # 7.49999881955


def run():
    bit_size = 8
    test_key = 'https://github.com/WokoLiu'
    bit_map = RedisBitMap(bit_size)
    func_list = build_hash_func_list(bit_size)
    bf = BloomFilter(bit_map, func_list)

    test_one(bf, test_key)
    test_one(bf, test_key)
    test_one(bf, test_key+'1')
    test_one(bf, test_key+'1')

if __name__ == '__main__':
    run()
