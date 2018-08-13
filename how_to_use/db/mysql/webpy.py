# -*- coding: utf-8 -*-
# @Time    : 2018/7/24 11:25
# @Author  : Woko
# @File    : webpy.py

"""使用 web.py 操作mysql数据库
当前只提供了一些简单操作，对应数据库表也非常简单

CREATE TABLE `test` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `value` varchar(32) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

"""

import web


def create_engine(db, host, port, user, pw, pooling=True):  # pylint: disable=R0913
    db = web.database(dbn='mysql', db=db, host=host, port=port, user=user,
                      pw=pw, pooling=pooling)
    return db

db = create_engine('test', '127.0.0.1', 3306, 'root', '12345678')

print type(db), db.__class__

print '\n支持的方法'
res = db.query('select * from test where id = ' + web.sqlquote(1))
print res[0] if res else 'query false'

res = db.select('test', vars={'id': 1}, what='value', where='id = $id', order='id asc')
print res[0] if res else 'select false'

res = db.where('test', id=1)
print res[0] if res else 'where false'

# res = db.insert('test', value='yoyoyo')
# print res

insert_data = [
    {'value': 111},
    {'value': '222'},
]
# res = db.multiple_insert('test', insert_data)
# print '这个地方的id会出错：',
# print res

res = db.update('test', where='id=1', value='iiii')
print res

res = db.delete('test', where='value=' + web.sqlquote('yoyoyo'))
print res
