# -*- coding: utf-8 -*-
# @Time    : 2018/7/6 18:43
# @Author  : Woko
# @File    : check_git_line.py

"""检查一个git项目中，某个用户的代码量及所占比例
必须在git根目录下执行
接收一个参数：要检测的用户名
"""

import commands
import os
import re
import sys


def check_line(pattern, file_name):
    count = all_count = 0
    file_data = commands.getoutput('git blame ' + file_name)
    for line in file_data.split('\n'):
        all_count += 1
        if pattern.match(line) is not None:
            count += 1
    # print count
    return count, all_count


def tree_file(base_path):
    for file_path, dir_list, file_list in os.walk(base_path):
        for file_name in file_list:
            if os.path.splitext(file_name)[1] == '.py':
                yield os.path.join(file_path, file_name)


if __name__ == '__main__':
    base_path = '.'
    user_name = sys.argv[1]  # 这是要检测的用户名
    pattern = re.compile('\w*\s\('+user_name)
    count = all_count = 0
    for file_path in tree_file(base_path):
        one, all_one = check_line(pattern, file_path)
        count += one
        all_count += all_one
    print count, all_count, float(count)/all_count*100
