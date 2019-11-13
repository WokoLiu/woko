# -*- coding: utf-8 -*-
# @Time     : 2019/11/13 22:22
# @Author   : Woko
# @File     : reflect.py

"""学习 Java 的反射"""

from flask import Flask

app = Flask(__name__)
app.debug = True


class Human:
    def __str__(self):
        return 'human'


class Man(Human):
    def __str__(self):
        return 'man'


class Woman(Human):
    def __str__(self):
        return 'woman'


human = Human()


@app.route('/human')
def get_human():
    return str(human)


@app.route('/change/<man>')
def change(man='Human'):
    global human
    human = globals()[man]()
    return 'change to ' + man


if __name__ == '__main__':
    app.run()

"""
# 测试效果
$ curl 127.0.0.1:5000/human
human%

$ curl 127.0.0.1:5000/change/Man
change to Man%

$ curl 127.0.0.1:5000/human
man%

$ curl 127.0.0.1:5000/change/Woman
change to Woman%

$ curl 127.0.0.1:5000/human
woman%
"""
