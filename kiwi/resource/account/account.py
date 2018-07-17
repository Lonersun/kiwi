# -*- coding:utf-8 -*-
from kiwi.core.resource.action import ResourceApi
from kiwi.route import route


class AccountApi(ResourceApi):

    route = '/account'

    def get(self):
        self.write("账户列表GET")

    def post(self):
        """
        创建账号
        :return:
        """
        self.write("账户创建POST")


class AccountSingleApi(ResourceApi):

    route = '/account/{account_id}'

    def get(self, account_id):
        self.write("账户详情GET")

    def put(self, account_id):
        params = self.req['params']
        body = self.req['body']
        self.req_out(body)


    def post(self, account_id):
        self.write("账户更新PUT")