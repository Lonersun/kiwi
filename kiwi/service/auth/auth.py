# -*- coding:utf-8 -*-
from kiwi import errors
from kiwi.model.account.account import Account


class AuthService(object):

    def __init__(self):
        self.account = Account()

    def login(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        mail = kwargs.get('mail')
        password = kwargs.get('password')
        account = self.account.find_one(mail=mail)
        if not account:
            raise errors.ErrorAccountNotFound()
        if password != account['password']:
            raise errors.ErrorInvalidArgument(message="password error.")
        return account

    def create(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        return self.account.insert(**kwargs)


