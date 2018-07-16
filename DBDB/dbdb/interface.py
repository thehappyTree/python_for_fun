# -*- coding:utf-8 -*-
# 定义DBDB
__auth__ = 'keweili'

from dbdb.binary_tree import BinaryTree
from dbdb.physical import Storage


class DBDB(object):
    def __init__(self, f):
        self._storage = Storage(f)
        self._tree = BinaryTree()

    def _assert_not_closed(self):
        if self._storage.closed:
            raise ValueError('Database closed')

    # 关闭数据库
    def close(self):
        self._storage.close()

    # 提交事务
    def commit(self):
        self._assert_not_closed()
        self._tree.commit()

    # 实现让该类的对象拥有dict的特性
    def __getitem__(self, key):
        # 索引获取值 key=value   db[key] ==> value
        self._assert_not_closed()
        return self._tree.get(key)

    def __setitem__(self, key, value):
        # key=value
        self._assert_not_closed()
        return self._tree.set(key, value)

    def __delitem__(self, key):
        self._assert_not_closed()
        return self._tree.pop(key)

    def __contains__(self, key):
        # key in db
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    def __len__(self):
        return len(self._tree)


if __name__ == '__main__':
    print("d")
    a = 1
    print(a)
