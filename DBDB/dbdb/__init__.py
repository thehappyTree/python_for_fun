# -*- coding:utf-8 -*-


import os
from dbdb.interface import DBDB


__all__ = ['DBDB', 'connect']


def connect(dbname):
    try:
        # 数据库以文件形式存储
        f = open(dbname, 'r+b')
    except IOError:
        fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, 'r+b')
    return DBDB(f)
