# -*- coding: utf-8 -*-
# @Time    : 2018/7/27 14:25
# @Author  : Woko
# @File    : bloom_filter.py

"""布隆过滤器，用于检测一个值是否在一个集合里
整体分三部分：1. 过滤器本体，2. 存储集合的工具，3. 一组哈希函数
参考文档：
简单介绍：http://www.10tiao.com/html/248/201805/2449231537/1.html
公式指导：https://blog.csdn.net/qq_18495465/article/details/78500472
python实现及redis.bitmap大小的选择：https://blog.csdn.net/Bone_ACE/article/details/53107018

TODO：
1. Memory的几个方式，增加lazy方式get/set
2. 考虑BitMap类里默认参数是否需要
"""

from hashlib import md5
import redis
from algorithm.build_hash import BitHash


class BitMap(object):
    """布隆过滤器使用的存储集合"""
    def __init__(self, bit_size, map_num=1, **kwargs):
        """
        :param bit_size: 总比特位数
        :param cap: bit map 总大小
        :param map_num: 集合个数
        """
        self.bit = bit_size
        self.cap = 1 << bit_size
        self.map_num = map_num
        self.__conf = kwargs

    def __getattr__(self, item):
        return self.__conf[item]

    def get_bit(self, value, map_id=0):
        """
        获取某比特位的值，支持同时存在多个map，但去第几个map里找需要外部指定
        :param value: 第几位
        :param map_id: 第几个map
        :return:
        """
        raise NotImplementedError

    def set_bit(self, value, map_id=0):
        """设置某比特位的值"""
        raise NotImplementedError


class MemoryListBitMap(BitMap):
    """在内存里，使用list来存储
    会占据超大量内存，无法处理超大量的数据（放在这里只是展示一下功能，实际上肯定不会使用这个）
    """
    def __init__(self, bit_size, map_num=1):
        super(MemoryListBitMap, self).__init__(bit_size, map_num)
        self.map_list = [[0] * self.cap] * map_num
        # self.map_list = []
        # for i in range(map_num):
        #     self.map_list.append([0] * self.cap)  # 1, 0, True, False，所占空间都是24byte

    def get_bit(self, value, map_id=0):
        if not 0 <= value < self.cap or not 0 <= map_id < self.map_num:
            return 0
        return 1 if self.map_list[map_id][value] else 0

    def set_bit(self, value, map_id=0):
        if not 0 <= value < self.cap or not 0 <= map_id < self.map_num:
            return None
        self.map_list[map_id][value] = 1
        print(self.map_list)


class MemoryStringBitMap(BitMap):
    """在内存里，使用string来存储
    会占据大量内存（大概是list的1/8）
    缺点是set_bit操作非常麻烦
    """
    def __init__(self, bit_size, map_num=1):
        super(MemoryStringBitMap, self).__init__(bit_size, map_num)
        self.map_list = ['0' * self.cap] * map_num

    def get_bit(self, value, map_id=0):
        if not 0 <= value < self.cap or not 0 <= map_id < self.map_num:
            return 0
        return 1 if self.map_list[map_id][value] == '1' else 0

    def set_bit(self, value, map_id=0):
        if not 0 <= value < self.cap or not 0 <= map_id < self.map_num:
            return None
        self.map_list[map_id] = self.map_list[map_id][:value]+'1'+self.map_list[map_id][value+1:]


class MemoryIntBitMap(BitMap):
    """在内存里，使用int来存储
    占用空间是string的 1/7.5，是list的 1/60（bit_size越大，越接近这个数字）
    速度也要快很多，但超大数量下还是会慢
    还不清楚是位移慢还是与或慢
    """
    def __init__(self, bit_size, map_num=1):
        super(MemoryIntBitMap, self).__init__(bit_size, map_num)
        self.map_list = [1 << self.cap] * map_num  # 是self.cap个二进制位的一个数

    def get_bit(self, value, map_id=0):
        """想到了三种方式，从上到下效率依次降低"""
        if not 0 <= value < self.cap or not 0 <= map_id < self.map_num:
            return 0
        return 1 if self.map_list[map_id] & (1 << (value-1)) else 0  # 直接判断这一位是不是有值
        # return (self.map_list[map_id] >> (value-1)) & 1  # 先右移，再与最末位与
        # return (self.map_list[map_id] >> (value-1)) % 2  # 先右移，再判奇偶

    def set_bit(self, value, map_id=0):
        """直接按位或"""
        if not 0 <= value < self.cap or not 0 <= map_id < self.map_num:
            return None
        self.map_list[map_id] |= (1 << (value-1))


class RedisBitMap(BitMap):
    """使用redis自带的bitmap
    超级快！
    """
    def __init__(self, bit_size, map_num=1, host='localhost', port=6379, db=0,  # pylint: disable=R0913
                 password=None, key='bloomfilter', expire=10):
        super(RedisBitMap, self).__init__(bit_size, map_num, key=key)
        self.redis = redis.StrictRedis(host=host, port=port, db=db, password=password)
        self.expire = expire

    def get_bit(self, value, map_id=0):
        """这里不需要对value和map_id做校验，redis会自动处理"""
        key = self.key + str(map_id)
        return self.redis.getbit(key, value)

    def set_bit(self, value, map_id=0):
        key = self.key + str(map_id)
        self.redis.setbit(key, value, 1)
        self.redis.expire(key, self.expire)


class BloomFilter(object):
    """布隆过滤器本体"""
    def __init__(self, bit_map, hash_func, map_num=1):
        """
        :param bit_map: 数据集合
        :param hash_func: 哈希函数组
        :param map_num: 数据集合个数
        """
        self.bit_map = bit_map
        self.hash_func = hash_func
        self.map_num = map_num

    def is_contain(self, value):
        """检测value是否在集合里"""
        if not value:
            return False
        try:
            value = md5(value).hexdigest()
        except TypeError:
            value = md5(value.encode('utf-8')).hexdigest()

        map_id = int(value[:2], 16) % self.map_num
        res = True
        for f in self.hash_func:
            loc = f.hash_str(value)
            res = res & self.bit_map.get_bit(loc, map_id)
        return res

    def insert(self, value):
        """将这个值插入集合"""
        try:
            value = md5(value).hexdigest()
        except TypeError:
            value = md5(value.encode('utf-8')).hexdigest()
        map_id = int(value[:2], 16) % self.map_num

        for f in self.hash_func:
            loc = f.hash_str(value)
            self.bit_map.set_bit(loc, map_id)


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
        print('yes', test_key)
    else:
        print('no', test_key)
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
    print(aa)  # 143165604
    print(bb)  # 1073741861
    print(cc)  # 8589934664
    print(cc / float(bb))  # 7.99999979138
    print(cc / float(aa))  # 59.9999889918
    print(bb / float(aa))  # 7.49999881955


def run():
    """入口函数"""
    bit_size = 8
    test_key = 'https://github.com/WokoLiu'
    map_num = 2
    bit_map = RedisBitMap(bit_size, map_num)
    func_list = build_hash_func_list(bit_size)
    bf = BloomFilter(bit_map, func_list, map_num)

    test_one(bf, test_key)
    test_one(bf, test_key)
    test_one(bf, test_key+'1')
    test_one(bf, test_key+'1')

if __name__ == '__main__':
    run()
