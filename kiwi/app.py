# -*- coding:utf-8 -*-
import logging.config
import pymongo
import os

from kiwi.core.utils.yamler import load_yaml_file
from tornado.ioloop import IOLoop
from tornado.web import Application
from kiwi.core.utils import importer
from kiwi.core.resource.action import ResourceApi
from kiwi.core.utils.validator import ValidatorRule
from kiwi.globals import global_context

logger = logging.getLogger(__name__)


class KiwiApp(object):

    resource_apis = []
    handles = []
    mongo = None

    def __init__(self, **kwargs):
        self.logger_config_path = kwargs.get('logger_config_path')
        self.config = kwargs.get('config', {})

    def load_resource(self):
        """

        :return:
        """
        # 加载参数规则
        rule_module = ValidatorRule(path=self.config['app_path'] + "/api_schema")
        rule_module.load_params_rule()
        rules = rule_module.rules
        # 加载路由
        resource_config = self.config.get('resources', [])
        base_class = ResourceApi
        for module_path in resource_config:
            for apis in importer.find_module_classes(module_path, base_class):
                # self.resource_apis.append(apis)
                route, module, rule_module = self.rebuild_api_module(apis, rules.get(apis.route, None))
                self.handles.append((route, module, dict(validator_rule=rule_module)))
                # self.handles.append((route, module))

    def rebuild_api_module(self, api, rule):
        """

        :param api:
        :param rule:
        :return:
        """
        route = api.route
        route_list = route.split('/')
        _route = ""
        for i in route_list:
            if i == "":
                _route += '/'
            elif "{" in i:
                _route += "(.*)/"
            else:
                _route += i + "/"
        if _route[-1] == '/':
            _route = _route[:-1]
        return _route, api, rule

    def bootstrap(self):
        """

        :return:
        """
        self.init_logger()
        self.init_mongo()
        global_context.db = self.mongo
        global_context.config = self.config
        global_context.push()

    def start(self):
        """

        :return:
        """
        config = self.config
        wsgi = config['wsgi']
        self.load_resource()
        settings = dict(
            debug=config.get('debug', False),
            cookie_secret=config.get('cookie_secret', 'errefdwqwertwherfwedqsa')
        )
        app = Application(self.handles, **settings)
        app.listen(wsgi.get('port', 8080))
        IOLoop.current().start()

    def init_mongo(self):
        """

        :return:
        """
        mongo_config = self.config['mongodb_service']['test']
        conn = pymongo.MongoClient(mongo_config.get('uri', 'mongodb://localhost:27017'))
        self.mongo = conn[mongo_config['database']]

    def init_logger(self):
        """

        :return:
        """
        pass
        # logging.config.fileConfig(self.logger_config_path)

    def init_mqtt(self):
        """

        :return:
        """
        pass


class KiwiLoader(object):

    @classmethod
    def bootstrap(cls, yaml_config_path=None, logger_config_path=None):
        server_config = load_yaml_file(yaml_config_path)
        server_config['app_path'] = os.path.dirname(os.path.dirname(__file__))
        app = KiwiApp(config=server_config, logger_config_path=logger_config_path)
        app.bootstrap()
        return app
