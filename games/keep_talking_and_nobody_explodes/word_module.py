# -*- coding: utf-8 -*-
# @Time     : 2022/5/2 18:25
# @Author   : Woko
# @File     : word_module.py

"""[keep talking and nobody explodes]
which column is the first one to specify
here is the number of word when I random 6 letter to filter all words
[8.074928, 8.079647, 8.077737, 8.076506, 8.077856]
so, whatever
"""

import random
import string
from collections import defaultdict

data = 'about after again below could every first found great house large learn never other place plant point right small sound spell still study their there these thing think three water where which world would write'
listdata = data.split(' ')

word_map_list = [defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int)]

for i in range(5):
    for word in listdata:
        word_map_list[i][word[i]] += 1


def random6():
    return ''.join(random.sample(string.ascii_lowercase, 6))


def run_for_count_times(times):
    count_for_all = [0] * 5
    print(count_for_all)
    for i in range(times):
        for i, count in enumerate(run_for_count()):
            count_for_all[i] += count
    print(list(map(lambda x: x / times, count_for_all)))


def run_for_count():
    random_str = random6()
    count_list = []
    for i, word_map in enumerate(word_map_list):
        count = 0
        for char in random_str:
            count += word_map.get(char, 0)
        count_list.append(count)
    
    print(random_str, count_list)
    return count_list


if __name__ == '__main__':
    run_for_count_times(1000000)
