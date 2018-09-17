# -*- coding: utf-8 -*-
# @Time    : 2018/7/26 10:53
# @Author  : Woko
# @File    : build_hash.py

"""hash函数H
密码学hash函数：https://www.cnblogs.com/block2016/p/5623902.html
几种构造方法：https://www.cnblogs.com/gj-Acit/archive/2013/05/06/3062628.html
这里实现了几种简单构造方式，实际构造时，还是要根据存储结构和关键字集合情况来写

TODO: BKDRHash，APHash，DJBHash，JSHash，RSHash，SDBMHash，PJWHash，ELFHash
"""


from hashlib import md5
import functools


def need_md5(func):
    """如果需要对待处理值先md5一下再操作，就加上这个装饰器"""
    @functools.wraps(func)
    def wrapper(self, value):
        value = md5(value).hexdigest()
        return func(self, value)
    return wrapper


class Hash(object):
    """作为下面实现的各种hash方法的基类
    hash函数接收的输入可能是数字，也可能是字符串
    但输出的一定是数字，不过可能因为太长所以输出十六进制的(如md5)
    """
    def __init__(self, **kwargs):
        self.__conf = kwargs

    def __getattr__(self, item):
        return self.__conf[item]

    def hash_int(self, value):
        raise NotImplementedError

    def hash_str(self, value):
        raise NotImplementedError


class RotateHash(Hash):  # pylint: disable=W0223
    """旋转法，需要考虑具体数据形态，再决定怎么转，一般用来协助其他hash方法
    所以这里做成装饰器类，在需要附加的地方直接使用就行
    """
    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(self, value):
            if isinstance(value, int):
                value = str(value)
            if isinstance(value, str):
                rotated_value = value[-1:] + value[:-1]
            else:
                rotated_value = value
            return func(self, rotated_value)
        return wrapper


class DirectHash(Hash):
    """直接寻址法，hash(K) = aK + C
    绝对没有冲突，但空间复杂性超高，适用于元素较少的情况
    """
    def hash_int(self, value):
        return value

    def hash_str(self, value):
        res = ''
        for i in value:
            res += str(ord(i))
        return int(res)


class AnalysisHash(Hash):  # pylint: disable=W0223
    """数字分析法，要预先知道待hash内容的结构及分布，不适合设计通用的hash算法"""
    pass


class ModHash(Hash):
    """除留余数法，hash(K) = K mod C
    一般要求常数C要接近或等于哈希表本身的长度，选素数时效果最好
    """
    def __init__(self, C):
        super(ModHash, self).__init__(C=C)

    def hash_int(self, value):
        return value % self.C

    def hash_str(self, value):
        return DirectHash().hash_str(value) % self.C


class SqrtMiddleHash(Hash):
    """平方取中法，对关键字取平方，然后取最中间的n位，n的选择取决于哈希表长度
    ps：这里是不是可以考虑下使用二进制位
    """
    def __init__(self, n):
        super(SqrtMiddleHash, self).__init__(n=n)

    def __middle(self, value):
        length = len(value) / 2
        return value[length-self.n/2:length+self.n/2+1]

    def hash_int(self, value):
        sqrt = str(value ** 2)
        return self.__middle(sqrt)

    def hash_str(self, value):
        sqrt = DirectHash().hash_str(value)
        res = self.__middle(str(sqrt))
        return int(res)


class FoldHash(Hash):
    """折叠法，适用于关键字位数较多，且分部大致均匀的
    这里先md5一下，然后再操作，以满足折叠法条件
    """
    def __init__(self, n):
        super(FoldHash, self).__init__(n=n)

    def hash_int(self, value):
        return self.hash_str(str(value))

    @RotateHash()
    @need_md5
    def hash_str(self, value):
        value = str(int(value, base=16))
        res = 0
        for i in range(0, len(value), self.n):
            res += int(value[i:i+self.n])
        return int(str(res)[-5:])


class RandHash(Hash):  # pylint: disable=W0223
    """随机数法，hash(K) = Rand(K)，其中Randy为伪随机数，真不知道有什么用"""
    pass


class BitHash(Hash):
    """保留其中的n位比特位，可以适用于除留取余法，折叠法，甚至平方取中法

    """
    def __init__(self, bit, seed):
        """
        :param bit: 比特位个数
        :param seed: 种子，用于减少冲突，不建议小于2
        """
        cap = 1 << bit  # 总容量，也等于 2 ** bit，但用位移更快
        operand = cap - 1
        super(BitHash, self).__init__(operand=operand, seed=seed)

    def hash_str(self, value):
        res = 0
        for i in value:
            res += self.seed * res + ord(i)
        return self.operand & res

    def hash_int(self, value):
        return self.hash_str(str(value))

if __name__ == '__main__':
    # hash_obj = FoldHash(5)
    # print hash_obj.hash_int(84388428)
    # print hash_obj.hash_str('yoyoyoyo')
    # print hash_obj.hash_str('yoyoyoyo')
    print(BitHash(31, 5).hash_str('yoyoyoyoyoyoyoyifjasidjfijisadjfijsidf'))
