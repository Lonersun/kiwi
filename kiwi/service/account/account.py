# -*- coding:utf-8 -*-
from kiwi.model.account.account import Account


class AccountService(object):

    def __init__(self):
        self.account = Account()

    def find(self):
        return self.account.find_one()

    def create(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        return self.account.insert(**kwargs)
