# -*- coding: utf-8 -*-
# @Time     : 2020/7/14 15:35
# @Author   : Woko
# @File     : rolling_variance.py

"""滚动方差
可用于实时流中计算方差
参考链接：https://blog.csdn.net/hnust_V/article/details/51763129
原理：原始公式中的分子化简 ∑(ai-av)^2 = ∑ai^2 - ∑2*ai*av + ∑a^2 = ∑ai^2 - 2*av*∑ai + n*av*av
注：上述公式中，ai 指第i个值，av 指所有数据的均值
得到最终公式：variance = (∑ai^2 - 2*av*∑ai + n*av*av) / n
其中 ∑ai^2 即为前 n 项平方和，∑ai 为前 n 项和，这些都是可以在实时流中计算的
由此，只需要一次循环即可得到结果，复杂度为 O(n)
"""

import numpy as np


def rolling_variance(data_list: list):
    """
    滚动方差计算逻辑
    :param data_list: 输入数据
    :return: 方差
    """

    # 前 n 项和
    data_sum = 0
    # 前 n 项平方和
    data_power_sum = 0

    # 仅需一次循环
    for i in data_list:
        data_sum += i
        data_power_sum += i ** 2

    # 数据长度
    length = len(data_list)
    # 均值
    average = data_sum / length

    return (data_power_sum - 2 * average * data_sum + length * average ** 2) / length


# 用于测试的数据
data = [1, 2, 3, 4, 5]

a = np.array(data)

# numpy 提供的计算方式
print(np.var(a))
# 原始公式
print(((a - np.mean(a)) ** 2).sum() / a.size)
# 滚动计算
print(rolling_variance(data))
