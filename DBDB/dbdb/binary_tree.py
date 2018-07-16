# -*- coding:utf-8 -*-
# 二叉树
import pickle


from dbdb.logical import LogicalBase, ValueRef


class BinaryNodeRef(ValueRef):
    def __init__(self):
        pass


class BinaryTree(LogicalBase):
    node_ref_class = BinaryNodeRef

    def __init__(self):
        pass

    def _get(self, node, key):
        while node is not None:
            if key < node.key:
                node = self._follow(node.left_ref)
            elif node.key < key:
                node = self._follow(node.right_ref)
            else:
                return self._follow(node.value_ref)
        raise KeyError

    @classmethod
    def from_node(cls, node, **kwargs):
        pass

