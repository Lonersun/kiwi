# -*- coding: utf-8 -*-
import json
from bson.json_util import (default as bson_object_default,
                            object_hook as bson_object_hook)


def to_lower(s):
    """

    :param s:
    :return:
    """
    return [i.lower() for i in s]


def json_dump(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, default=bson_object_default,
                      encoding='utf-8')
