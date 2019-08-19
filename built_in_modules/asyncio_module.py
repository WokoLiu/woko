# -*- coding: utf-8 -*-
# @Time    : 2019-08-08 13:53
# @Author  : Woko
# @File    : asyncio_module.py

"""temp commit"""

import asyncio
import datetime
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    task1 = asyncio.create_task(say_after(1, 'hello'))

    task2 = asyncio.create_task(say_after(2, 'world'))

    print(f'started at {time.strftime("%X")}')

    # await say_after(1, 'hello')
    # await say_after(2, 'world')
    await task1
    print('in it ')
    await task2

    print(f'finished at {time.strftime("%X")}')


# asyncio.run(main())


async def display_date():
    loop = asyncio.get_running_loop()
    print(type(loop), loop, loop.__dict__)
    end_time = loop.time() + 5.0

    while 1:
        print(datetime.datetime.now())
        if (loop.time() + 1.0) >= end_time:
            break
        await asyncio.sleep(1)


# asyncio.run(display_date())


async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f'Task {name}: Compute factorial({i})...')
        await asyncio.sleep(1)
        f += 1
    print(f'Task {name}: factorial({number}) = {f}')


async def gather_main():
    await asyncio.gather(
        factorial('A', 2),
        factorial('B', 3),
        factorial('C', 4)
    )


asyncio.run(gather_main())
