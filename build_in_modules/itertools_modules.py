# -*- coding: utf-8 -*-
# @Time    : 2018/7/16 15:03
# @Author  : Woko
# @File    : itertools_modules.py

"""itertools，这里面实现的都是完整类，而不是单纯方法
官方文档：https://docs.python.org/2.7/library/itertools.html
官方文档的部分中文解释：https://www.jb51.net/article/55626.htm
廖雪峰 https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001415616001996f6b32d80b6454caca3d33c965a07611f000

无限迭代器：
count(start=0, step=1): 一个无限+1的生成器，可以调整start和step
cycle(iterable): 无限次迭代出入的可迭代对象
repeat(object,times=None): 重复返回传入的object无限次或times次

简单迭代器：
chain(*iterables): 将传入的多个可迭代对象按传入顺序连接起来，变成一个大迭代器
compress(data, selectors): 根据真值表selectors来filter，决定返回data里的哪些值
groupby(iterable, key=None): 将第一个参数里，连续且重复的值返回，判定连续的方式可由第二个key函数来说明，功能类似sorted的key

dropwhile(func, iterable): 第一个参数是个真值函数，迭代第二个参数并对每个值进行真值判断，当第一次为False时，将此值以及之前迭代过的值全部丢掉，对剩余内容进行迭代
talewhile(func, iterable): 与dropwhile对应，当第一次为False时，取这个节点及前面全部节点

ifilter(func_or_None, sequence): 就是普通filter的生成器实现，同样如果func_orNone写None的话，每个判断都认为是True
ifilterfalse(func_or_None, sequence): 普通filter的生成器实现，并对真值判断函数取反，注意如果func_no_None写None的话，每个判断都认为是False

islice: slice的生成器实现，可以对生成器进行切片，切完之后返回的还是生成器
imap(): map的生成器实现
starmap(): imap的一种调用方式，imap(func, p,q) 等价于 starmap(func, zip(p, q))
izip(): 在python2里，是zip()的生成器版本
izip_longest(): 如果传入的几个iterables长度不同，迭代次数为长度最大的

【数学】排列组合里的生成器：
product(*iterables, repeat=1): 求iterables的笛卡尔积元组，repeat表示之前传入的参数重复几遍
permutations(iterable, r=None): 排列，从len(iterable)个元素中任取r or len(iterable)个不同元素(r <= len(iterable))的排列，即A(m, n)
combinations(iterable, r=None): 组合，从len(iterable)个元素中任取r or len(iterable)个不同元素(r <= len(iterable))的组合，即C(m, n)
combinations_with_replacement: 组合，但允许一组中含有多个相同元素

这是itertools里的唯一一个方法
tee(): 将一个iterable变成n个iterable，注意如果原始iterable是生成器，那么调用完此方法后，原iterable和新iterable，只有一个能使用，即如果使用了原，那么新的就会全部为空，如果使用了新(即使只使用了一个)，原也会已消耗殆尽
"""
import itertools


# itertools.count 效果等价于此方法
def count(start=0, step=1):
    x = start
    while True:
        yield x
        x += step


# itertools.chain 效果等价于此方法
def chain(iterables):
    for x in iterables:
        for y in x:
            yield y


# itertools.product 效果等价于此方法
def product(*args, **kwargs):
    # print 'lala', map(tuple, args)
    pools = map(tuple, args) * kwargs.get('repeat', 1)
    # print 'wowo', pools
    result = [[]]
    for pool in pools:
        # for x in result:
        #     for y in pool:
        #         print 'x', x, 'y', y, 'x+[y]', x + [y]
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)


def test_infinite():
    # for i in itertools.count():
    # for i in itertools.cycle('abc'):
    for i in itertools.repeat('d', 10):
        print i

print '\ncompress'
x = itertools.compress(range(4), (1, 0, 0, 1))
y = itertools.compress(range(4), (False, True, True, False))
print list(x)
print list(y)

print '\ndropwhile'
drop = itertools.dropwhile(lambda i: i < 5, (1,2,3,7,8,9,4,5,6,0))
print list(drop)

print '\ngroupby'
for k, v in itertools.groupby('XXXYYZZZZYY'):
    print k, list(v)
for k, v in itertools.groupby('AaaBbBccDDDeE', lambda c: c.upper()):
    print k, list(v)

print '\nifilter'
flt = itertools.ifilter(lambda c: c < 5, (1, 4, 6, 8, 3))
print list(flt)
fltf = itertools.ifilterfalse(lambda c: c < 5, (1, 4, 6, 8, 3))
print list(fltf)
fltf2 = itertools.ifilterfalse(None, (1,2,3))
print list(fltf2)

print '\nimap'
imap1 = itertools.imap(lambda x,y: x*y, range(4), range(3, 100))
print list(imap1)
print 'starmap'
smap1 = itertools.starmap(lambda x,y: x*y, ((1,2), (3,4), (5,6)))
print list(smap1)
print 'imap 和 starmap 互换'
test_map = lambda x, y: x * y
map_data = (range(4), range(3, 100))

ismap1 = itertools.imap(test_map, *map_data)
print list(ismap1)
ismap2 = itertools.starmap(test_map, zip(*map_data))
print list(ismap2)
ismap3 = itertools.starmap(test_map, zip(range(4), range(3, 100)))
print list(ismap3)

print '\nchain'
z = 'ABCDEF'
a = itertools.chain(z)
b = itertools.chain.from_iterable(z)
c = chain(z)
print a.next(), b.next(), c.next()

print '\nproduct'
prod1 = itertools.product('abc', 'def', repeat=2)
print list(prod1)
prod2 = product('abc', 'def', repeat=2)
print list(prod2)
prod3 = itertools.product(range(2), repeat=3)
print list(prod3)

print '\npermutations'
pm1 = itertools.permutations('abcdef', 2)
print list(pm1)

print '\ncombinations'
cb1 = itertools.combinations('abc', 2)
print list(cb1)
cb2 = itertools.combinations_with_replacement('abc', 2)
print list(cb2)

print '\ntee'
origin = itertools.ifilter(None, 'asdfghjkl')
tee1 = itertools.tee(origin, 2)
print list(tee1[0])
print list(origin)
tee2 = itertools.tee(tee1[1], 2)  # 这里tee1[1]由于没有使用，可以当做origin给第二个测试来使用
print list(tee1[1])
print list(tee2[0])