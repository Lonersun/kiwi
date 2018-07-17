# -*- coding:utf-8 -*-
from functools import partial
from werkzeug.local import LocalStack, LocalProxy, LocalManager


class LocalContext(object):
    def __init__(self, ctx_stack=None, **data):
        if ctx_stack is None:
            ctx_stack = LocalStack()
        self.ctx_stack = ctx_stack
        if data:
            for k, o in data.iteritems():
                setattr(self, k, o)

    def push(self):
        self.ctx_stack.push(self)

    def pop(self):
        rv = self.ctx_stack.pop()
        assert rv is self, 'Popped wrong local context.  (%r instead of %r)' \
                           % (rv, self)

    def __enter__(self):
        self.push()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.pop()

    def lookup_object(self, name):
        top = self.ctx_stack.top
        if top is None:
            raise RuntimeError('working outside of context')
        return getattr(top, name)

    @property
    def has_context(self):
        return self.ctx_stack.top is not None

    def local_proxy(self, name):
        return LocalProxy(partial(self.lookup_object, name))

    def fork_context(self, **local_data):
        return LocalContext(self.ctx_stack, **local_data)


_sentinel = object()


class _AppCtxGlobals(object):

    def get(self, name, default=None):
        return self.__dict__.get(name, default)

    def pop(self, name, default=_sentinel):
        if default is _sentinel:
            return self.__dict__.pop(name)
        else:
            return self.__dict__.pop(name, default)

    def setdefault(self, name, default=None):
        return self.__dict__.setdefault(name, default)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __repr__(self):
        return object.__repr__(self)
