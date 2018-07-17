# -*- coding:utf-8 -*-
from kiwi.core.utils.ctx import LocalContext, LocalStack
from kiwi.core.utils.registry import Registry

_global_registry = Registry()
_global_ctx_stack = LocalStack()

global_context = LocalContext(_global_ctx_stack)

db = global_context.local_proxy('db')
config = global_context.local_proxy('config')
