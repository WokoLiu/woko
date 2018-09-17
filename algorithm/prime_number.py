# -*- coding: utf-8 -*-
# @Time    : 2017/9/29 11:25
# @Author  : Woko
# @File    : prime_number.py

"""
质数相关算法
参考资料：
http://www.cnblogs.com/hardsoftware/p/5935850.html
http://www.cnblogs.com/SivilTaram/p/5914075.html
https://baike.baidu.com/item/埃拉托斯特尼筛法
"""
import math


prime_set = ()


def is_prime(num):
    """
    检测一个数是不是质数的基本方法，从1到4不断高效
    1. 从2到num-1，依次做除法，有能整除的就不是质数
    2. 从2到num/2，依次做除法，有能整除的就不是质数
    3. 从2到sqrt(num)，依次做除法，有能整除的就不是质数
    4. 从2到sqrt(num)，用其中所有质数依次做除法，有能整除的就不是质数
    :param num:
    :return:
    """

    # 这个判断是不是需要，根据具体情况来吧
    # if num == 1:
    #     return False

    # for x in xrange(2, num):
    # for x in xrange(2, num/2+1):
    for x in range(2, int(math.sqrt(num))+1):
    # global prime_set
    # for x in prime_set:
        if num % x == 0:
            return False
    return True


def the_max_prime_area(n):
    """
    获取第n个质数可能的最大值，公式是：第n个质数 < n*ln(n) + n*ln(ln(n)) (n>=6)
    :param n:
    :return:
    """
    if n < 6:  # 这个公式在 n >= 6时才生效
        return 14  # 第六个质数是13，所以随便给个 > 13 的数
    else:
        return int(n*math.log(n) + n*math.log(math.log(n)))


def get_first_n_prime(n):
    """
    获取自然数中第n个质数，有几种方法，按序数从小到大效率依次提高
    1. 试除法：while True 循环，检测每个数
    2. 试除法：while True 循环，只检测奇数，不检测偶数
    3. 筛法：埃拉托斯特尼筛法：从2开始标记当前最小质数的所有倍数，之后下一个未标记的最小数就是质数，
        一直把[2, sqrt(n)+1]内所有质数的倍数都做上标记，剩下的数里前n个未被标记的数都是质数，找到第n个即可
    4. 筛法：优化筛法
    :param n:
    :return:
    """
    # return first_n_by_trial_division(n)
    return first_n_by_sieve_of_eratosthenes(n)


def first_n_by_trial_division(n):
    """
    试除法求自然数中第n个质数
    :param n:
    :return:
    """
    count = 1  # 这里已有的一个质数是2
    x = 1  # 这里虽然从1开始，但是进去后会先+2再计算，也就是已经默认了1是合数2是质数
    while count < n:
        x += 2
        if is_prime(x):
            count += 1
            # print 'the %d prime is %d' % (count, x)
        # x += 1
    return x


def first_n_by_sieve_of_eratosthenes(n):
    """
    使用埃拉托斯特尼筛法
    1. 对全量数据做一个数组，用True/False来标记是不是质数
    2. 不使用数组，而是使用一个比特位来标记一个数是不是质数
    3. 局部筛法：
        1. 保存下(0, sqrt(max_num)) 内所有质数
        2. 在(sqrt(max_num), max_num)范围内分段用之前保存的素数去判断，并记录下筛出的质数的数量
        3. 根据机器cache的大小选择合适的分段大小
    :param n:
    :return:
    """
    # 获取所需列表的最大值
    max_num = the_max_prime_area(n)

    # 构建全数组
    basic_list = []
    for x in range(max_num+1):  # 从0开始往数组里放，当然第0个元素我们不用管
        if x % 2 == 0:
            basic_list.append(False)
        else:
            basic_list.append(True)
    # print basic_list

    base_num = 3  # 构建数组时2已经筛过了，现在从3开始筛
    while base_num * base_num <= max_num:  # 当当前数的平方超过最大值时，跳出筛的循环
        if basic_list[base_num]:  # 只有质数需要筛
            product_num = base_num * base_num  # 因为 base_num**2 之前的合数都已经被比base_num小的质数标记掉了
            while product_num <= max_num:  # 标记 < max_num 的全部符合条件的数
                basic_list[product_num] = False
                product_num += base_num + base_num  # 加两次是因为，2的倍数已经都干掉了，加一次一定是奇数，不需要判断直接跳就行
        base_num += 2  # 跳过偶数，只看奇数

    count = 1  # 从1开始是因为默认2已经是质数，加入计数了，这样下面的循环才可以从3开始只取奇数
    for x in range(3, max_num+1, 2):
        if basic_list[x]:
            count += 1
        if count == n:
            return x
    return False


if __name__ == '__main__':
    the_first_n = 1000
    # print is_prime(67)
    print(get_first_n_prime(the_first_n))
    # print the_max_prime_area(1000)
