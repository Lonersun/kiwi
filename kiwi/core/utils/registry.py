# -*- coding:utf-8 -*-

_missing = object()


class Registry(object):

    def __init__(self, definitions={}):
        self._storage = {}
        self.extend(definitions)

    def add(self, name, definition):
        self._storage[name] = definition

    def all(self):
        return self._storage

    def extend(self, definitions):
        for name, definition in dict(definitions).items():
            self.add(name, definition)

    def clear(self):
        self._storage.clear()

    def get(self, name, default=None):
        return self._storage.get(name, default)

    def remove(self, *names):
        for name in names:
            self._storage.pop(name, None)

    def __contains__(self, item):
        return item in self._storage

    def __getattr__(self, item):
        return self.get(item)


class LRUCacheRegistry(Registry):
    lru_ttl = 300
