# -*- coding: utf-8 -*-
# @Time    : 2017/10/2 12:12
# @Author  : Woko
# @File    : kmp.py

"""
kmp算法(俗称看毛片算法)，是一个快速匹配字符串的算法，时间复杂度O(n+m)
给自己的记录：光看代码没用，理解清楚每一步的原理后，代码自己就可以写出来

参考文件：
1. http://blog.csdn.net/yutianzuijin/article/details/11954939/
2. http://kenby.iteye.com/blog/1025599
3. http://www.cnblogs.com/SYCstudio/p/7194315.html
4. https://baike.baidu.com/item/kmp%E7%AE%97%E6%B3%95/10951804
5. http://blog.csdn.net/power721/article/details/6132380

参考文件说明：
文件1里有几张图特别适合理解匹配失败时的处理方案，可以最后看
文件2有一段如何肉眼识别next列表的描述，适合next到底如何生成
文件3里有动图，适合理解kmp整个过程
文件4是百度百科，里面讲了newnext，属于完全理解了kmp后再优化的部分
文件5提供了overlay这个函数名，并且提供了kmp的进阶：DFA

"""


def overlay(pattern):
    """
    对模式字符串进行预处理，获取模式字符串各长度前缀子串里，前缀后缀的最长匹配长度
    也就是各帖子里说的next数组，或称为f数组
    :param pattern: str 要预处理的模式字符串
    :return: f: list
    """
    f = [0]  # 若记下标为i，此list表示模式字符串里子串长度为i时，其前缀后缀的最长匹配长度
    print pattern
    for i in xrange(1, len(pattern)):  # 这里是在遍历模式字符串，字符串下标从0开始，所以这个从1开始的遍历是从第二个字符开始判断的
        j = i  # 标记在模式字符串里用作对比的位置
        print '\n当前已知：', f, pattern[:len(f)]
        print '开始分析下一个字符，j=%d' % j, pattern[:j], pattern[j]
        print '即将对比的是：', j, pattern[i], '和', f[j-1], pattern[f[j-1]]
        while pattern[i] != pattern[f[j-1]] and j > 0:  # 注意这个地方是用pattern[i]来进行对比的，而不是pattern[j]
            print '这两个不匹配，需要重新确定j'
            print 'before, j =', j, pattern[:j+1]
            print 'after, j = f[j-1] = f[%d-1] = %d' % (j, f[j-1]), pattern[:f[j-1]+1]
            j = f[j-1]  # 这一步很关键，原理见参考文件1
            if j != 0:
                print '现在即将再次对比：', j, pattern[j], '和', f[j-1], pattern[f[j-1]]
            else:
                print '已对比到模式字符串开头，停止继续对比，这里的值是 0'
        if j == 0:
            f.append(0)
        else:
            print '匹配成功，结果是：', f[j-1] + 1
            f.append(f[j-1] + 1)
        print '结果是：', f, '对应模式字符串是', pattern[:len(f)]
    return f


def kmp(target, pattern):
    next_list = overlay(pattern)
    j = 0
    for i in xrange(0, len(target)):
        print '即将匹配的是这俩数：', target[i], pattern[j]
        if target[i] == pattern[j]:
            print '当前匹配成功！：%s, %s' % (target[:i+1], pattern[:j+1])
            j += 1
        else:
            print '匹配失败，重新尝试'
            print 'before, j=%d' % j
            j = next_list[j]
            print 'after, j=%d' % j
        if j == len(pattern):
            return i-j+1
    return False


if __name__ == '__main__':
    target = 'abaabaabbabaaabaabbabaab'
    pattern = 'abaabbabaab'
    real_next = [0, 0, 1, 1, 2, 0, 1, 2, 3, 4, 5]
    # print overlay(pattern)
    # print real_next
    print kmp(target, pattern)
