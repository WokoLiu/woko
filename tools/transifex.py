# -*- coding: utf-8 -*-
# @Time    : 2019-07-25 10:14
# @Author  : Woko
# @File    : transifex.py

"""翻译群一个老哥给的原始脚本，统计翻译排名"""

import getpass
import requests
import concurrent.futures
from collections import Counter
# from multiprocessing import shared_memory

# usr = input('Your username(DO NOT USE EMAIL):')
# pwd = getpass.getpass()
token = '1/c80e2e29d12fa05e77b5a45d5321de7592cb9d4a'
usr = 'api'
pwd = f'{token}'
name = 'Woko'
rc_res = requests.get('https://www.transifex.com/api/2/project/python-newest/resources/', auth=(usr, pwd))
rc_list = [item['slug'] for item in rc_res.json()]
# strings_owner = shared_memory.ShareableList([])
strings_owner = []


def fetch_rc(slug):
    res = requests.get('https://www.transifex.com/api/2/project/python-newest/resource/%s/translation/zh-cn/strings/?details' % slug, auth=(usr,pwd)).json()
    strings_owner.extend([item['user'] for item in res if item is not ''])


with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    print('Waiting for counting %d resources.\n' % len(rc_list))
    executor.map(fetch_rc, rc_list)

stat = Counter(strings_owner)
del stat['']
print('---- TOP 10 TRANSLATORS ---')

for item in stat.most_common(10):
    print('%-20s - %5d string' % (item[0], item[1]))
print('\nYou are #%d.' % ([i[0] for i in stat.most_common()].index(name) + 1))

