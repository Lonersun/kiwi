# -*- coding: utf-8 -*-
from kiwi.globals import db


class BaseMode(object):

    collection = ""

    def __init__(self):
        self.db = db

    def find(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        return self.db[self.collection].find(kwargs)

    def find_one(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        return self.db[self.collection].find_one(kwargs)

    def insert(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        return self.db[self.collection].insert(kwargs)

    def update(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        spec = {
            "_id": kwargs.pop('id')
        }
        return self.db[self.collection].update(kwargs, {'$set': spec})