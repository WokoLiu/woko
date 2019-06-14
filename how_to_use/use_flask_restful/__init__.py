# -*- coding: utf-8 -*-
# @Time    : 2019-06-14 15:03
# @Author  : Woko
# @File    : __init__.py

from flask import Flask

from how_to_use.use_flask_restful.restful import api

app = Flask(__name__)
app.debug = True

api.init_app(app)


@app.route('/')
def index():
    return 'index'


if __name__ == '__main__':
    app.run()
