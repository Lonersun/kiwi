# -*- coding: utf-8 -*-
from tornado.web import HTTPError

HTTP_CODE_SERVER_ERROR = 500
HTTP_CODE_API_ERROR = 400


class SYSError(HTTPError):

    code = 500
    name = 'SystemError!'
    message = 'System error!'


class APIError(HTTPError):

    code = 400
    name = 'Api Error'
    message = 'api error.'
    zh_message = "API 调用错误."

    def __init__(self, message=None, code=None, name=None, zh_message=None, *args, **kwargs):

        if message:
            self.message = message
        if code:
            self.code = code
        if name:
            self.name = name
        if zh_message:
            self.zh_message = zh_message
        kwargs['reason'] = self.zh_message
        super(APIError, self).__init__(status_code=400, log_message=self.message, *args, **kwargs)


class ErrorInvalidArgument(APIError):

    code = 401001
    message = "invalid argument."
    zh_message = "参数错误."


class ErrorAccountNotFound(APIError):

    code = 401002
    message = "account not found."
    zh_message = "账号没有找到."


class ErrorContentTypeNotSupport(APIError):

    code = 401003
    message = "content type error."
    zh_message = "content type error."


class ErrorSystem(APIError):

    code = 500
    message = "system error."
    zh_message = "系统异常."