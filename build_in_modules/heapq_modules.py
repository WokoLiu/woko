# -*- coding: utf-8 -*-
# @Time    : 2018/7/9 15:50
# @Author  : Woko
# @File    : heapq_modules.py

"""
nlargest, nsmallest: 找到最大或最小的n个元素
heapify: 最小堆排一个list，a[0]永远最小，heapq.heappop(a)可以弹出最小的一个，然后重新调整以维持最小堆
heappush: 往heap里塞一个值，并重排堆
heappop: 从heap里拿出最小的一个值，并重排堆

heapreplace(heap, item): 先把heap[0] pop出来，然后push进item，注意heap一定要是个heapify后的堆，不能是随便一个list
heappushpop(heap, item): 先push进item，然后pop出最小的heap[0]，与heapreplace顺序相反，同样要求heap是个堆
merge: 是这个代码的生成器版本：sorted(itertools.chain(*iterables))，但要求传入的每个list都是已经从小到大排好序了的
"""
import heapq
import itertools

sea = [2, 2, 3, 45, 5623, 23, 1, 2124, -12, 45, 6, -21]

print heapq.nlargest(5, sea)
print heapq.nsmallest(3, sea)

data3 = [
    {'pid': '0', 'value': '1'},
    {'pid': '8', 'value': '2'},
    {'pid': '8', 'value': '3'},
    {'pid': '1', 'value': '4'},
    {'pid': '10', 'value': '5'},
    {'pid': '2', 'value': '6'},
    {'pid': '2', 'value': '7'},
    {'pid': '0', 'value': '8'},
    {'pid': '3', 'value': '9'},
    {'pid': '3', 'value': '10'},
]
print heapq.nlargest(5, data3, key=lambda x: int(x['pid']))


print '\n几个函数的用法'
print '原数据', sea
heapq.heapify(sea)
print '排序后', sea
heapq.heapreplace(sea, 888)
print '替换最小值', sea
last_pop = heapq.heappop(sea)
print 'pop', sea
print last_pop
heapq.heappushpop(sea, 887)
print '快速重新push', sea


multy_list = ([1, 3, 5, 7], [0, 2, 4, 8], [5, 10, 15, 20], [], [25])
print list(heapq.merge(*multy_list))
print sorted(itertools.chain(*multy_list))
