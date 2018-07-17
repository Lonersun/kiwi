# -*- coding:utf-8 -*-

import cerberus
from cerberus import Validator

v = Validator()

# 允许值(枚举值) allowed

v.schema = {'role': {'type': 'list', 'allowed': ['agent', 'client', 'supplier']}}

v.validate({'role': ['agent', 'supplier']})
# True

v.validate({'role': ['intern']})
# False

v.schema = {'role': {'type': 'string', 'allowed': ['agent', 'client', 'supplier']}}
v.validate({'role': 'supplier'})
# True

v.validate({'role': 'intern'})
# False

v.schema = {'a_restricted_integer': {'type': 'integer', 'allowed': [-1, 0, 1]}}
v.validate({'a_restricted_integer': -1})
# True

v.validate({'a_restricted_integer': 2})
# False


# allof 所有条件都满足
v.schema = {
    "age": {
        "allof": [{'min': 5, 'max': 10}, {'min': 8, 'max': 20}]
    }
}
v.validate({'age': -1})
# False
v.validate({'age': 12})
# False
v.validate({'age': 8})
# True
v.validate({'age': 30})
# False

# anyof 满足其中一个条件，或者两个条件都满足
v.schema = {
    "age": {
        "anyof": [{'min': 5, 'max': 10}, {'min': 8, 'max': 20}]
    }
}
v.validate({'age': -1})
# False
v.validate({'age': 12})
# True
v.validate({'age': 8})
# True
v.validate({'age': 30})
# False


# noneof 两个条件都不满足
v.schema = {
    "age": {
        "noneof": [{'min': 5, 'max': 10}, {'min': 8, 'max': 20}]
    }
}
v.validate({'age': -1})
# True
v.validate({'age': 12})
# False
v.validate({'age': 8})
# False
v.validate({'age': 30})
# True

# oneof 只满足其中一个条件
v.schema = {
    "age": {
        "oneof": [{'min': 5, 'max': 10}, {'min': 8, 'max': 20}]
    }
}
v.validate({'age': -1})
# False
v.validate({'age': 12})
# True
v.validate({'age': 8})
# False
v.validate({'age': 30})
# False

# dependencies 依赖
v.schema = {
    "a": {"required": False},
    "b": {"required": False},
    "c": {"required": False, 'dependencies': ['a']},
}
v.validate({'a': 1, 'b': 1})
# True
v.validate({'a': 1, 'c': 1})
# True
v.validate({'b': 1, 'c': 1})
# False 当传入c的时候必须传入a，c依赖a

v.schema = {
    "a": {"required": False},
    "b": {"required": False},
    "c": {"required": False, 'dependencies': {'a': [1, 2]}},
}




