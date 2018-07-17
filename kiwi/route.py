# -*- coding:utf-8 -*-


class Route(object):
    """
    """
    _routes = []

    def __init__(self, regexp):
        """

        :param regexp:
        """
        self._regexp = regexp

    def __call__(self, handler):
        """

        :param handler:
        :return:
        """
        self._routes.append((self._regexp, handler))
        return handler

    @classmethod
    def get_routes(cls):
        return cls._routes

route = Route
