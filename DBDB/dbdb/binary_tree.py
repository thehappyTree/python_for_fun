# -*- coding:utf-8 -*-
# 二叉树
import pickle


from dbdb.logical import LogicalBase, ValueRef


class BinaryNode(object):
    @classmethod
    def from_node(cls, node, **kwargs):
        length = node.length
        if 'left_ref' in kwargs:
            length += kwargs['left_ref'].length - node.left_ref.length
        if 'right_ref' in kwargs:
            length += kwargs['right_ref'].length - node.right_ref.length
        return cls(
            left_ref=kwargs.get('left_ref', node.left_ref),
            key=kwargs.get('key', node.key),
            value_ref=kwargs.get('value_ref', node.value_ref),
            right_ref=kwargs.get('right_ref', node.right_ref),
            length=length,
                   )

    def __init__(self, left_ref, key, value_ref, right_ref, length):
        self.left_ref = left_ref
        self.key = key
        self.value_ref = value_ref
        self.right_ref = right_ref
        self.length = length

    def store_refs(self, storage):
        self.value_ref.store(storage)
        self.left_ref.store(storage)
        self.right_ref.store(storage)


class BinaryNodeRef(ValueRef):

    def prepare_to_store(self, storage):
        if self._referent:
            self._referent.store_refs(storage)

    @property
    def length(self):
        if self._referent is None and self._address:
            raise RuntimeError('wrong')
        if self._referent:
            return self._referent.length
        else:
            return 0

    def __init__(self):
        pass


class BinaryTree(LogicalBase):
    node_ref_class = BinaryNodeRef

    def __init__(self):
        pass

    def _insert(self, node, key, value_ref):
        # 当前表是空的生成一个新的树
        if node is None:
            new_node = BinaryNode(
                self.node_ref_class(), key, value_ref, self.node_ref_class(), 1
            )
        elif key < node.key:
            new_node = BinaryNode.from_node

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

