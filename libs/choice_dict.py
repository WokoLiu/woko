# -*- coding: utf-8 -*-
# @Time    : 2019-08-16 11:20
# @Author  : Woko
# @File    : choice_dict.py

"""
一个 key 可以存多个值，但取的时候只随机从中取一个
"""

from random import choice

from werkzeug.datastructures import MultiDict


class ChoiceDict(MultiDict):
    def __getitem__(self, key):
        if key in self:
            lst = dict.__getitem__(self, key)
            if len(lst) > 0:
                return choice(lst)
        return None
