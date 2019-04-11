# -*- coding: utf-8 -*-
# @Time    : 2019/4/11 13:57
# @Author  : Woko
# @File    : spring.py

"""随机喷泉⛲️"""

import random
import time
from pprint import pprint


class MatrixNode(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.up = None
        self.down = None
        self.value = self

    def add_right(self, value):
        self.right = value

    def add_left(self, value):
        self.left = value

    def add_up(self, value):
        self.up = value

    def add_down(self, value):
        self.down = value


class Nozzle(MatrixNode):
    """biu biu biu"""

    def __init__(self, start=0.5, min=2, max=6, wait=3):
        self.start = start
        self.min = min
        self.max = max
        self.wait = wait
        self._current = 0
        self._schedule = []
        self._schedule_len = 0
        super(Nozzle, self).__init__()

    @property
    def current(self):
        return self._current

    def click(self) -> int:
        # have schedule
        if self._schedule:
            if self.current < self._schedule_len:  # on the schedule
                self._current += 1
                return self._schedule[self.current]
            else:  # end the schedule
                self._schedule = []
                self._current = 0
                self._schedule_len = 0
                return self.click()

        # build a schedule
        return self._build_schedule()

    def _build_schedule(self) -> int:
        self._current = 0

        # don't start
        if random.random() >= self.start:
            self._schedule = []
            self._schedule_len = 0
            return 0

        during = random.randint(self.min, self.max)
        self._schedule = [x for x in range(during, 0, -1)] + [0] * self.wait
        self._schedule_len = len(self._schedule) - 1
        return self._schedule[self.current]


class Fountain(object):
    """a real fountain rectangle"""

    def __init__(self, hight=10, weight=10):
        self.data = []
        for i in range(hight):
            row = []
            for j in range(weight):
                row.append(Nozzle())
            self.data.append(row)
        self._current = [[0] * weight] * hight

    @property
    def current(self):
        return self._current

    def click(self):
        data = []
        for i in self.data:
            row = []
            for j in i:
                row.append(j.click())
            data.append(row)
        self._current = data
        return self.current


if __name__ == '__main__':
    fountain = Fountain()
    for _ in range(100):
        time.sleep(1)
        pprint(fountain.click())
        print('')
