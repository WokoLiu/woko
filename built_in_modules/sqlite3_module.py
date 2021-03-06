# -*- coding: utf-8 -*-
# @Time    : 2019-06-11 11:26
# @Author  : Woko
# @File    : sqlite3_module.py

import sqlite3

conn = sqlite3.connect('sqlite.db')


def create_table():
    conn.execute('''CREATE TABLE COMPANY
           (ID INT PRIMARY KEY     NOT NULL,
           NAME           TEXT    NOT NULL,
           AGE            INT     NOT NULL,
           ADDRESS        CHAR(50),
           SALARY         REAL);''')


def insert_data():
    conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (1, 'Paul', 32, 'California', 20000.00 )")

    conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (2, 'Allen', 25, 'Texas', 15000.00 )")

    conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )")

    conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )")


def simple_select():
    cursor = conn.execute('SELECT id, name, address, salary  from COMPANY')
    for row in cursor:
        print('ID = ', row[0])
        print('NAME = ', row[1])
        print('ADDRESS = ', row[2])
        print('SALARY = ', row[3], '\n')

    conn.commit()

    conn.close()


def with_select():
    try:
        with sqlite3.connect('sqlite.db') as con:
            cur = con.cursor()
            cur.execute(
                'INSERT INTO COMPANY (ID, NAME, AGE, ADDRESS, SALARY) VALUES(?, ?, ?, ?, ?)',
                (5, 'Woko', 25, 'Top', 100.00))
            con.commit()
            print('Record successfully added')
    except Exception as e:
        con.rollback()
        print(e)
        print('error in insert operation')
    finally:
        con.close()


def with_insert():
    with sqlite3.connect('sqlite.db') as con:
        cur = con.cursor()
        cur.execute(
            'INSERT INTO COMPANY (ID, NAME, AGE, ADDRESS, SALARY) VALUES(?, ?, ?, ?, ?)',
            (5, 'Woko', 25, 'Top', 100.00))
        con.commit()
