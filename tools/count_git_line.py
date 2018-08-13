# -*- coding: utf-8 -*-
# @Time    : 2018/7/6 18:43
# @Author  : Woko
# @File    : count_git_line.py

"""检查一个git项目中，每个人的代码量及占比
须在对应git环境下执行

也可只检测某个人的，接收一个传入参数做用户名
"""

import commands
import os
import re
import fnmatch
from collections import defaultdict


def count_one(file_name, pattern):
    """检测某个人的代码行数"""
    count = all_count = 0
    file_data = commands.getoutput('git blame ' + file_name)
    for line in file_data.split('\n'):
        all_count += 1
        if pattern.match(line) is not None:
            count += 1
    # print count
    return count, all_count


def tree_file(base_path):
    """遍历某目录下所有文件，并返回绝对路径名"""
    for file_path, _, file_list in os.walk(base_path):
        for file_name in file_list:
            # if os.path.splitext(file_name)[1] == '.py':
            if fnmatch.fnmatch(file_name, '*.py'):
                yield os.path.join(file_path, file_name)


everyone_lines = defaultdict(int)


def count_everyone(file_name):
    """计算所有人的代码行数"""
    all_count = 0
    global everyone_lines
    file_data = commands.getoutput('git blame ' + file_name)
    for line in file_data.split('\n'):
        if line:
            all_count += 1
            user = line[line.index('(')+1:].split(' ', 1)[0]
            everyone_lines[user] += 1
    return all_count


def run(base_path, user_name):
    """获取某个人的代码行数"""
    pattern = re.compile(r'\w*\s\(' + user_name)
    count = all_count = 0
    for file_path in tree_file(base_path):
        one, all_one = count_one(file_path, pattern)
        count += one
        all_count += all_one
    print count, all_count, float(count) / all_count * 100


def run_all(base_path):
    all_count = 0
    for file_path in tree_file(base_path):
        all_count += count_everyone(file_path)
    print '总代码量：', all_count
    if everyone_lines['Not']:
        not_commit = everyone_lines['Not']
        del everyone_lines['Not']
        print '未提交：', not_commit
    for user, count in everyone_lines.iteritems():
        print user, ': ', count, (float(count)/all_count*100)

if __name__ == '__main__':
    base_path = '.'

    # 检测某个人的
    # user_name = sys.argv[1]  # 这是要检测的用户名
    # run(base_path, user_name)

    # 检测所有人的
    run_all(base_path)