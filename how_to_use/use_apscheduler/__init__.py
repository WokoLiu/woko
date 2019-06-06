# -*- coding: utf-8 -*-
# @Time    : 2019-06-06 14:54
# @Author  : Woko
# @File    : __init__.py

import datetime
import logging
import time

from apscheduler.events import *
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.ERROR)

jobstores = {
    'default': SQLAlchemyJobStore(
        url='mysql+pymysql://root:12345678@localhost:3306/test')
}

# sched = BlockingScheduler()
sched = BackgroundScheduler(jobstores=jobstores)
sched._logger = logging


def my_job():
    print(datetime.datetime.now())
    print(1 / 0)


def append_file():
    with open('file.txt', 'a') as f:
        f.write(str(datetime.datetime.now()))
        f.write('\n')


def listener(event: SchedulerEvent):
    if isinstance(event, JobExecutionEvent) and event.exception:
        print('got an exception', event.exception)


sched.add_job(my_job, 'interval', seconds=3)
sched.add_job(append_file, 'interval', seconds=5)
sched.add_listener(listener, EVENT_JOB_ERROR | EVENT_JOB_EXECUTED)
sched.start()

x = 30
while x > 0:
    print(x)
    x -= 1
    time.sleep(3)
