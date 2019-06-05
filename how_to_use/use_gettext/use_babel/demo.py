# -*- coding: utf-8 -*-
# @Time    : 2019/4/15 14:41
# @Author  : Woko
# @File    : demo.py

"""用 flask_babel 写了个 demo
BABEL_TRANSLATION_DIRECTORIES 指定存放翻译文件的目录，可以是个list
defaut_domain 是 .mo 文件的文件名
babel.localeselector 指定每次请求中，如何判定使用何种语言

还写了个小脚本用于处理语言文件：
* 创建新语言文件：./translate.sh init zh
* 更新：./translate.sh update
* 编译成 .mo 文件：./translate.sh build
"""

from flask import Flask
from flask import request
from flask_babel import Babel
from flask_babel import gettext as _

app = Flask(__name__)

app.config.setdefault('BABEL_TRANSLATION_DIRECTORIES', 'translations')
babel = Babel(app, default_locale='en', default_domain='messages',
              configure_jinja=False)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['en', 'zh', 'ja'])


@app.route('/')
def index():
    return _('hello, index')


@app.route('/wow')
def wow():
    return _('wow')


@app.route('/cn')
def scn():
    return _('这是中文哦')


@app.route('/ja')
def sja():
    return _('これは日本語ですよ')


if __name__ == '__main__':
    app.run('0.0.0.0', 8888, debug=True)
