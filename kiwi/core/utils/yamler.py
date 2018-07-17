# -*- coding:utf-8 -*-
import io
import yaml


def load_yaml_file(path):
    """

    :param path:
    :return:
    """
    data = None
    with io.open(path, 'r', encoding='utf-8') as reader:
        data = yaml.load(reader)
    return data
