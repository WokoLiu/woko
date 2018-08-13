# -*- coding: utf-8 -*-
# @Time    : 2018/7/24 17:47
# @Author  : Woko
# @File    : sqlalchemy_sth.py

"""使用sqlalchemy操作mysql
我真的不喜欢这个玩意
再见吧
"""

from sqlalchemy import Column, String, INT, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TeNoSt(Base):
    __tablename__ = 'test'

    id = Column(INT(), primary_key=True, autoincrement=True)
    value = Column(String(32), nullable=False, default='')

    def update(self, info_dict):
        for key in info_dict:
            setattr(self, key, info_dict[key])

engine = create_engine('mysql://root:12345678@localhost:3306/test')

DBSession = sessionmaker(bind=engine)

session = DBSession()

new_one = TeNoSt(value='ahhhhh')
session.add(new_one)
session.commit()

this_one = session.query(TeNoSt).filter(TeNoSt.id == 1).one()

print type(this_one)
print this_one, this_one.id, this_one.value

this_one.update({'value': 'laiii'})
session.commit()

still_this_one = session.query(TeNoSt).filter(TeNoSt.id == 1).one()
print still_this_one.id, still_this_one.value

ready_to_delete = session.query(TeNoSt).filter(TeNoSt.value == 'ahhhhh')
if ready_to_delete:
    session.delete(ready_to_delete[0])
session.commit()

session.close()
