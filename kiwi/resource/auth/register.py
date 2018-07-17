# -*- coding:utf-8 -*-
from kiwi.core.resource.action import ResourceApi
from kiwi import errors


class RegisterApi(ResourceApi):

    route = '/auth/register'

    def get(self):
        raise errors.ErrorAccountNotFound()
        # self.write("注册GET")

    def post(self):
        """

        :return:
        """
        docs = self.req['body']


        self.write("注册POST")
