# -*- coding:utf-8 -*-
import logging
import tornado.web
from tornado.web import HTTPError
import sys
from tornado.escape import json_encode, to_unicode, json_decode

from kiwi import errors
from kiwi.core.utils.validator import validator_factory
from kiwi.core.utils.utils import json_dump


class ResourceApi(tornado.web.RequestHandler):

    logger = logging.getLogger(__name__)
    route = None
    req = {}

    def initialize(self, **kwargs):
        """

        :return:
        """
        self.validator_rule = kwargs.get('validator_rule', {})

    def prepare(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        try:
            params, body = self.rebuild_params(self.validator_rule)
            self.req['params'] = params
            self.req['body'] = body
        except errors.APIError, e:
            self.send_error(status_code=errors.HTTP_CODE_API_ERROR, exc_info=sys.exc_info())

    def send_error(self, status_code=500, **kwargs):
        """

        :param status_code:
        :param kwargs:
        :return:
        """
        self.set_status(status_code)
        self.load_response_header()
        _, error, _ = kwargs.get('exc_info')
        if hasattr(error, 'code'):
            error_code = error.code
        else:
            error_code = status_code
        response_body = {
            "error_code": error_code,
            "error_message": error.message,
        }
        self.finish(response_body)

    def options(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        self.set_status(204)
        self.load_response_header()

    def rebuild_params(self, validator_rule):
        """

        :param validator_rule:
        :return:
        """
        # 获取query body 参数
        req = self.request


        method = req.method.lower()
        params = {}
        if req.arguments:
            for key, value in req.query_arguments.iteritems():
                if isinstance(value, list):
                    params[key] = to_unicode(value[0])
                else:
                    params[key] = None
        body = {}
        if method in ['post', 'put'] and req.body:
            if not self.request.headers.get('Content-Type'):
                raise errors.ErrorContentTypeNotSupport()
            content_type = self.request.headers['Content-Type'].lower()
            if content_type != 'application/json':
                raise errors.ErrorContentTypeNotSupport()
            body = json_decode(req.body)
        # 执行参数校验
        # 获取规则
        rule = validator_rule.get(method, {})
        params = validator_factory.validator(rule.get('query_rule', {}), params)
        body = validator_factory.validator(rule.get('body_rule', {}), body)
        return params, body

    def req_out(self, context):
        """

        :return:
        """
        self.load_response_header()
        self.finish(json_dump(context))

    def load_response_header(self):
        """

        :return:
        """
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT")
        self.set_header("Access-Control-Allow-Headers", ('Content-Type'))
        self.set_header("Access-Control-Max-Age", "1728000")

