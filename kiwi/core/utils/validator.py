# -*- coding:utf-8 -*-
import os
import glob
import re

from bson import ObjectId
from cerberus import Validator

from kiwi.core.utils import convert, yamler
from kiwi import errors


class ValidatorRule(object):

    path = ""
    rules = {}

    def __init__(self, path):
        """

        :param path:
        """
        self.path = path

    def load_params_rule(self):
        """

        :return:
        """
        _PKG_ROOT = os.path.join(self.path)
        definitions_yml = yamler.load_yaml_file(_PKG_ROOT + '/definitions.yml')
        for pkg_dir in filter(os.path.isdir, glob.glob(self.path + '/*')):
            for mod_file in glob.glob('%s/*.yml' % pkg_dir):
                mod_name = os.path.basename(mod_file).rstrip('.yml')
                resource_text = yamler.load_yaml_file(mod_file)
                self.rebuild_rule(resource_text)
                resources = []

    def rebuild_rule(self, rule):
        """

        :param rule:
        :return:
        """
        for _rule in rule:
            rule_base = {}
            for api_method, api in _rule.get('apis', {}).iteritems():
                body_rule = {}
                query_rule = {}
                for api_rule in api.get('parameters', []):
                    api_rule = self.change_rule_convert(api_rule)

                    position = api_rule.pop('in')
                    if position == 'body':
                        body_rule[api_rule.pop('name')] = api_rule
                    elif position == 'query':
                        query_rule[api_rule.pop('name')] = api_rule
                rule_base[api_method] = {
                    'body_rule': body_rule,
                    'query_rule': query_rule,
                }
            self.rules[_rule['route_base']] = rule_base

    @classmethod
    def change_rule_convert(cls, api_rule):
        """

        :param api_rule:
        :return:
        """
        api_rule.pop('note')
        if api_rule.get('coerce'):
            api_rule['coerce'] = cls._get_coerce(api_rule['coerce'])
        api_rule['type'] = cls._convert_type_names(api_rule['type'])
        return api_rule

    @classmethod
    def _convert_type_names(cls, t):
        """

        :param t:
        :return:
        """
        t = t.lower()
        _map = {
            'object_id': 'objectid',
            'objectid': 'objectid',

            'int': 'integer',
            'integer': 'integer',

            'str': 'string',
            'string': 'string',
            'basestring': 'string',
            'unicode': 'string',
            'bytes': 'binary',

            'bool': 'boolean',
            'boolean': 'boolean',
            'date': 'date',
            'datetime': 'datetime',

            'float': 'float',
            'number': 'number',
            'long': 'integer',

            'set': 'set',
            'dict': 'dict',
            'list': 'list',
        }
        return _map.get(t)

    @classmethod
    def _get_coerce(cls, t):
        """

        :param t:
        :return:
        """
        t = t.lower()
        _map = {
            'object_id': convert.to_object_id,
            'objectid': convert.to_object_id,
            'int': convert.to_int,
            'integer': convert.to_int,
            'str': convert.to_unicode,
            'string': convert.to_unicode,
            'unicode': convert.to_unicode,
            'basestring': convert.to_unicode,
            'bool': bool,
            'boolean': bool,
            'float': convert.to_float,
            'long': convert.to_long,
            'list': list,
        }
        return _map.get(t)


class SchemaValidator(Validator):

    def _validate_type_objectid(self, value):
        """

        :param value:
        :return:
        """
        if isinstance(value, ObjectId):
            return True

        if re.match('[a-f0-9]{24}', str(value)):
            return True


class ValidatorFactory(object):

    @classmethod
    def validator(cls, schema, document):
        """

        :param schema:
        :param document:
        :return:
        """
        v = SchemaValidator()
        is_ok = v.validate(document, schema)
        if not is_ok:
            message = ""
            for k, e in v.errors.iteritems():
                message += k + ":" + str(e) + "."
            raise errors.ErrorInvalidArgument(message=message)
        return v.document

validator_factory = ValidatorFactory()