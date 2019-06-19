# -*- coding: utf-8 -*-
# @Time    : 2019-06-18 14:47
# @Author  : Woko
# @File    : TheGameOfLife.py

"""The Game of Life by John Horton Conway
about coroutines
codes from "effective python"
https://github.com/bslatkin/effectivepython/blob/master/example_code/item_40.py

游戏样式：
  0   |   1   |   2   |   3   |   4
----- | ----- | ----- | ----- | -----
-*--- | --*-- | --**- | --*-- | -----
--**- | --**- | -*--- | -*--- | -**--
---*- | --**- | --**- | --*-- | -----
----- | ----- | ----- | ----- | -----

游戏规则：
任意尺寸的二维网格中，每个细胞都处在 ALIVE 和 EMPTY 两种状态之一，
时钟每走一步，生命游戏就前进一轮，每个细胞在下一轮是否存活，取决于周围的8个细胞
规则是：(参见 game_logic 函数)
1. 若本细胞存活且周围存活细胞数小于2或大于3，则本细胞下一轮死亡
2. 若本细胞死亡且周围存活细胞数等于3，则本细胞下一轮重生
3. 其他情况，本细胞存活状态不变
"""
from collections import namedtuple
from typing import Union, Generator, overload, Optional, List, Tuple

# 生存状态
ALIVE = '*'  # 生存
EMPTY = '-'  # 死亡

# 以下三个对象，都是**协程迭代过程中返回的对象**，代表不同的含义
# 对协程来说，因为迭代返回内容的实际处理者都是外部调用方
# 因此需要用不同的对象来表示不同的含义以及期待的返回

# 保存这一对坐标值，希望得到的回复是此节点的State
Query = namedtuple('Query', ('y', 'x'))  # y 是纵坐标，x 是横坐标
# 保存着一对坐标值和一个状态值，表示此坐标的细胞在下一轮的状态
Transition = namedtuple('Transition', ('y', 'x', 'state'))
# 这个对象不包含内容，只表示整个游戏完成了一轮
TICK = object()

# 这两个是类型标注，用于标注和注释，不影响正常代码逻辑
State = str  # 枚举类型咋标注啊，其实就是ALIVE/EMPTY
Coordinate = int  # 坐标值


def count_neighbors(y: Coordinate, x: Coordinate) \
        -> Generator[Query, State, int]:
    """计算自己周围有几个存活的
    :param y: 当前细胞纵坐标
    :param x: 当前细胞横坐标
    :return 作为生成器，会返回 Query 对象，并期待返回此位置的状态
    :return 最终返回：当前细胞周围8个格子里，存活的细胞数
    """
    # 这是8个方位，yield 出 Query 后，返回的结果是 State
    n_ = yield Query(y + 1, x + 0)  # North
    ne = yield Query(y + 1, x + 1)  # Northeast
    e_ = yield Query(y + 0, x + 1)  # East
    se = yield Query(y - 1, x + 1)  # Southeast
    s_ = yield Query(y - 1, x + 0)  # South
    sw = yield Query(y - 1, x - 1)  # Southwest
    w_ = yield Query(y + 0, x - 1)  # West
    nw = yield Query(y + 1, x - 1)  # Northwest

    # 这里保存的是周围各个细胞的状态
    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    return count


def test_count_neighbors():
    """测试 count_neighbors 函数"""
    it = count_neighbors(10, 5)
    q1 = next(it)  # get the first query
    print('q1', q1)
    q2 = it.send(ALIVE)  # send q1 state, get q2
    print('q2', q2)
    q3 = it.send(ALIVE)
    print('q3', q3)
    q4 = it.send(ALIVE)
    print('q4', q4)
    q5 = it.send(ALIVE)
    print('q5', q5)
    q6 = it.send(ALIVE)
    print('q6', q6)
    q7 = it.send(ALIVE)
    print('q7', q7)
    q8 = it.send(ALIVE)
    print('q8', q8)

    try:
        count = it.send(ALIVE)  # send q8 state, get count
    except StopIteration as e:  # 当协程里没有下一个 yield 时，会触发这个异常
        print('Count:', e.value)  # 此时，返回值需要从异常里取(看 StopIteration 定义)


def game_logic(state: State, neighbors: int) -> State:
    """游戏基本逻辑（这个不是生成器啦）
    :param state: 当前细胞状态
    :param neighbors: 周围8个细胞中，有几个活着
    :return: 当前细胞下一轮的状态
    """
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY  # Die: too few
        elif neighbors > 3:
            return EMPTY  # Dei: too many
    else:
        if neighbors == 3:
            return ALIVE  # Regenerate 重生
    return state


@overload
def step_cell(y: Coordinate, x: Coordinate) \
        -> Generator[Query, State, None]: ...


@overload
def step_cell(y: Coordinate, x: Coordinate) \
        -> Generator[Transition, None, None]: ...


def step_cell(y, x):
    """单个细胞前进一轮要做的事
    如果最后 return Transition 的话，就必须显式处理这个值
    比如把 simulate 里改成这样：

    >>> res = yield from step_cell(y, x)
    >>> yield res

    而 yield Transition 并且 return None 的话，可以省掉这个处理
    """
    state = yield Query(y, x)  # 请求自己当前的状态
    # 获取自己周围有几个还活着
    neighbors = yield from count_neighbors(y, x)
    # 判断自己在下一轮的状态
    next_state = game_logic(state, neighbors)
    # 下一轮里自己的状态
    yield Transition(y, x, next_state)


def test_step_cell():
    it = step_cell(10, 5)
    q0 = next(it)
    print('Me:     ', q0)
    q1 = it.send(ALIVE)
    print('Q1:     ', q1)
    q2 = it.send(ALIVE)
    print('Q2:     ', q2)
    q3 = it.send(ALIVE)
    print('Q3:     ', q3)
    q4 = it.send(ALIVE)
    print('Q4:     ', q4)
    q5 = it.send(ALIVE)
    print('Q5:     ', q5)
    q6 = it.send(ALIVE)
    print('Q6:     ', q6)
    q7 = it.send(ALIVE)
    print('Q7:     ', q7)
    q8 = it.send(ALIVE)
    print('Q8:     ', q8)
    t1 = it.send(EMPTY)
    print('Outcome:', t1)
    it.close()


def simulate(height: int, width: int) \
        -> Generator[Union[Query, Transition, object], Optional[State], None]:
    """对一个二维平面，对其中每个细胞执行 step_cell
    注意，只要外部允许，这个函数可以永远一步一步运行下去
    :param height: 平面高度
    :param width: 平面宽度
    """
    while True:
        for y in range(height):
            for x in range(width):
                # 对每个细胞执行一遍 step_cell，并且 yield 回新的状态
                yield from step_cell(y, x)
        yield TICK  # 表示完成了整一轮


class Grid(object):
    """平面网格类"""

    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        # 是个二维数组，保存完整的网格
        self.rows = []  # type: List[List[State]]
        for _ in range(self.height):
            # 初始化时，都是 EMPTY
            self.rows.append([EMPTY] * self.width)

    def query(self, y: Coordinate, x: Coordinate) -> State:
        """查询某个坐标的细胞状态
        用于应对 Query 类
        """
        return self.rows[y % self.height][x % self.width]

    def assign(self, y: Coordinate, x: Coordinate, state: State) -> None:
        """修改某个坐标上细胞的状态"""
        self.rows[y % self.height][x % self.width] = state

    def alive(self, coordinate: List[Tuple[Coordinate, Coordinate]]) -> None:
        """将某些坐标点设置为 ALIVE
        用于游戏初始化
        """
        for y, x in coordinate:
            self.assign(y, x, ALIVE)

    def __str__(self):
        res = ''
        for row in self.rows:
            for cell in row:
                res += cell
            res += '\n'
        return res


def live_a_generation(grid: Grid, sim: Generator) -> Grid:
    """对 simulate 协程内返回的对象进行处理，让整个游戏前进一轮
    这个函数不是协程，而是使用协程的最外侧调用方
    它直接持有协程的生成器对象，并对协程中生成的对象做处理
    :param grid: 游戏网格对象，保存着当前所有细胞的状态
    :param sim: simulate 协程的生成器对象，用于迭代这个协程
    :return progeny: 过完这一轮之后，下一轮的完整网格状态
    """
    progeny = Grid(grid.height, grid.width)
    # 让生成器运行起来
    # 仔细分析可知此时拿到的是第一个细胞在 step_cell 的第一句
    # 也就是 Query(0,0)
    item = next(sim)
    # 依次取得协程生成的对象，并处理，反正一共就三种可能
    while item is not TICK:  # TICK 表示这一轮完毕，可以返回了
        if isinstance(item, Query):
            # 查询这个细胞的状态，并返回
            state = grid.query(item.y, item.x)
            item = sim.send(state)
        else:  # Must be a Transition
            # 标记这个点在下一轮的状态
            progeny.assign(item.y, item.x, item.state)
            item = next(sim)  # Transition 没有期待返回，因此不需要 send
    return progeny


def build_glider_grid():
    """构建 glider 网格，是一种叫做 滑翔机 的经典形状
    整体每过4个回合，会往右下角移动一格，如下
        0     |     1     |     2     |     3     |     4
    ---*----- | --------- | --------- | --------- | ---------
    ----*---- | --*-*---- | ----*---- | ---*----- | ----*----
    --***---- | ---**---- | --*-*---- | ----**--- | -----*---
    --------- | ---*----- | ---**---- | ---**---- | ---***---
    --------- | --------- | --------- | --------- | ---------
    """
    grid = Grid(5, 9)
    grid.alive([(0, 3), (1, 4), (2, 2), (2, 3), (2, 4)])
    return grid


class ColumnPrinter(object):
    """用于把网格横向打印"""

    def __init__(self):
        # 元素是 Grid 直接 str 后的内容
        self.columns = []  # type: List[str]

    def append(self, data: str) -> None:
        self.columns.append(data)

    def __str__(self):
        """构建成横向结构然后输出"""
        row_count = 1
        for data in self.columns:
            row_count = max(row_count, len(data.splitlines()) + 1)
        rows = [''] * row_count
        for j in range(row_count):
            for i, data in enumerate(self.columns):
                line = data.splitlines()[max(0, j - 1)]
                if j == 0:
                    padding = ' ' * (len(line) // 2)
                    rows[j] += padding + str(i) + padding
                else:
                    rows[j] += line
                if (i + 1) < len(self.columns):
                    rows[j] += ' | '
        return '\n'.join(rows)


def run():
    columns = ColumnPrinter()  # 构建printer
    grid = build_glider_grid()  # 构建原始网格
    sim = simulate(grid.height, grid.width)  # 获得simulate 生成器
    columns.append(str(grid))
    for i in range(8):  # 迭代8轮
        grid = live_a_generation(grid, sim)  # 迭代一轮并获取之后的grid
        columns.append(str(grid))
    print(columns)


run()

# 最终结果是这样的
'''
    0     |     1     |     2     |     3     |     4     |     5     |     6     |     7     |     8    
---*----- | --------- | --------- | --------- | --------- | --------- | --------- | --------- | ---------
----*---- | --*-*---- | ----*---- | ---*----- | ----*---- | --------- | --------- | --------- | ---------
--***---- | ---**---- | --*-*---- | ----**--- | -----*--- | ---*-*--- | -----*--- | ----*---- | -----*---
--------- | ---*----- | ---**---- | ---**---- | ---***--- | ----**--- | ---*-*--- | -----**-- | ------*--
--------- | --------- | --------- | --------- | --------- | ----*---- | ----**--- | ----**--- | ----***--
'''
