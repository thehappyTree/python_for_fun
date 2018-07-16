# -*- coding:utf-8 -*-


class ValueRef(object):
    def __init__(self, referent=None, address=0):
        self._referent = referent
        self._address = address

    def prepare_to_store(self, storage):
        pass

    @staticmethod
    def referent_to_string(referent):
        return referent.encode('utf-8')

    @staticmethod
    def string_to_referent(string):
        return string.decode('utf-8')

    @property
    def address(self):
        return self._address

    def get(self, storage):
        if self._referent is None and self._address:
            self._referent = self.string_to_referent(storage.read(self._address))

    def store(self, storage):
        if self._referent is not None and not self._address:
            self.prepare_to_store(storage)
            self._address = storage.write(self.referent_to_string(self._referent))


class LogicalBase(object):
    node_ref_class = None
    value_ref_class = ValueRef

    def __init__(self, storage):
        self._tree_ref = None  # 该声明没屁用，只是为了消除Pycharm的警告
        self._storage = storage
        self._refresh_tree_ref()

    def commit(self):
        pass

    def _refresh_tree_ref(self):
        self._tree_ref = self.node_ref_class(
            address=self._storage.get_root_address()
        )

    def get(self, key):
        if not self._storage.locked:
            self._refresh_tree_ref()
        return self._get(self._follow(self._tree_ref), key)

    def set(self, key, value):
        if not self._storage.locked:
            self._refresh_tree_ref()
        self._tree_ref = self._insert(
            self._follow(self._tree_ref), key, self.value_ref_class(value)
        )

    def pop(self, key):
        if self._storage.lock():
            self._refresh_tree_ref()
        self._tree_ref = self._delete(
            self._follow(self._tree_ref), key
        )

    def _follow(self, ref):
        return ref.get(self._storage)

    def __len__(self):
        pass
