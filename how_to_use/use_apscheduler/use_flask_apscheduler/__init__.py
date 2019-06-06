# -*- coding: utf-8 -*-
# @Time    : 2019-06-06 16:16
# @Author  : Woko
# @File    : __init__.py

"""轻量级的定时任务执行方式
此脚本可以直接运行，会每隔5秒输出一次当前时间
scheduler api 的测试可以直接用 ./scheduler_api.sh
其中的 V29rbzpMaXU= 是直接把 Woko:Liu base64 得来的
"""

import datetime

from apscheduler.events import EVENT_JOB_ERROR
from flask import Flask
from flask_apscheduler import APScheduler
from flask_apscheduler.api import get_jobs
from flask_apscheduler.auth import HTTPBasicAuth

app = Flask(__name__)
app.debug = False
sched = APScheduler()


# ====== 下面几行是开启 scheduler_api 的，选用
class SchedulerApiConfig:
    SCHEDULER_API_ENABLED = True
    SCHEDULER_ALLOWED_HOSTS = [sched.host_name]  # 限制可调用的 hosts，默认无限制
    SCHEDULER_API_PREFIX = '/scheduler'  # 默认就是这个
    SCHEDULER_AUTH = HTTPBasicAuth()  # 可以自己配置


app.config.from_object(SchedulerApiConfig())


# 认证方式可以自行配置
@sched.authenticate
def authenticate(auth):
    if auth['username'] == 'Woko' or auth['password'] == 'Liu':
        return True
    else:
        return False


# ====== 上面几行是开启 scheduler_api 的，选用


# 定时运行的任务
def now():
    print(datetime.datetime.now())


# 任务监控
def listener(event):
    if event.exception:
        print('got an exception', event.exception)


sched.add_listener(listener, EVENT_JOB_ERROR)
sched.init_app(app)
sched.add_job('job1', now, trigger='interval', seconds=5)
sched.start()


@app.route('/')
def index():
    return 'index'


@app.route('/jobs')
def show_job():
    return get_jobs()


if __name__ == '__main__':
    app.run()
