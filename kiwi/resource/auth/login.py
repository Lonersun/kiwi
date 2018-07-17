# -*- coding:utf-8 -*-
from kiwi.core.resource.action import ResourceApi
from kiwi.service.auth.auth import AuthService


class LoginApi(ResourceApi):

    route = '/auth/login'

    def get(self):
        self.write("登录GET")

    def post(self):
        """

        :return:
        """
        body = self.req['body']
        account_id = self.get_secure_cookie('account_id')
        if account_id:
            self.req_out({"ok": True})
            return
        account = AuthService().login(**body)
        self.set_secure_cookie("account_id", str(account['_id']))
        response = {
            "ok": True,
            "account_id": str(account['_id']),
            "account_name": account['name']
        }
        self.req_out(response)


class LogoutApi(ResourceApi):

    route = '/auth/logout'

    def get(self):
        # raise
        self.write("注销GET")

    def post(self):
        """

        :return:
        """
        self.clear_cookie('account_id')
        response = {
            "ok": True,
        }
        self.req_out(response)