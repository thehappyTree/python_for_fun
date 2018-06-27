# -*- coding:utf-8 -*-
# 定义DBDB

from dbdb.binary_tree import BinaryTree


class DBDB(object):
    def __init__(self, f):
        a = BinaryTree()

    def _assert_not_closed(self):
        pass

    # 关闭数据库
    def close(self):
        pass

    # 提交事务
    def commit(self):
        pass

    # 实现让该类的对象拥有dict的特性
    def __getitem__(self, item):
        # 索引获取值 key=value
        pass

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    def __contains__(self, key):
        # key in db
        pass

    def __len__(self):
        pass



if __name__ == '__main__':
    print("d")
