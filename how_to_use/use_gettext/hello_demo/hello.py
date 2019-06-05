# -*- coding: utf-8 -*-
# @Time    : 2019-06-05 11:53
# @Author  : Woko
# @File    : hello.py

"""
参考这个文章：https://mp.weixin.qq.com/s/NgY6Ek8TEBcyg8vhnpYdRw
系统安装 gettext 后就可以直接使用

具体用法：
1. 写代码，如下，须用 gettext() 包住待翻译字符串
2. 从 .py 文件中提取字符串到 .pot `xgettext -o hello.pot hello.py`
3. 设置 .pot 文件的字符集为 UTF-8
4. 提取创建好要存放语言文件的目录 translations/zh/LC_MESSAGES
5. 从 .pot 生成语言文件 .po `msginit -i hello.pot -o translations/zh/hello.po -l zh`
6. 填写 .po 文件，完善所有字符串
7. 用 .po 文件生成 .mo 文件 `msgfmt translations/zh/hello.po -o translations/zh/hello.mo`
8. 可以运行代码了（日语部分同理）

注：.pot 文件和 .mo 文件一般是在 .gitignore 里的，不提交到 git 上
"""

import gettext

print('hello world')

# 中文
zh = gettext.translation('hello', 'translations', languages=['zh'])
zh.install()
print(zh.gettext('hello world'))

# 日语
jp = gettext.translation('hello', 'translations', languages=['jp'])
jp.install()
_ = jp.gettext
print(_('hello world'))
