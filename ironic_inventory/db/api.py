# -*- encoding: utf-8 -*-

"""Database API for CRUD on inventory servers.
"""

import abc

import six

from oslo_config import cfg
from oslo_db import api as db_api


_BACKEND_MAPPING = {'sqlalchemy': 'ironic_inventory.db.sqlalchemy.api'}
IMPL = db_api.DBAPI.from_config(cfg.CONF, backend_mapping=_BACKEND_MAPPING, lazy=True)


def get_instance():
    return IMPL


@six.add_metaclass(abc.ABCMeta)
class Connection(object):

    @abc.abstractmethod
    def add_server(self, **kwargs):
        pass

    @abc.abstractmethod
    def remove_server(self, uuid):
        pass

    @abc.abstractmethod
    def get_all_servers(self):
        pass

    @abc.abstractmethod
    def get_matching_servers(self, **kwargs):
        pass

    @abc.abstractmethod
    def get_single_server_match(self, **kwargs):
        pass

    @abc.abstractmethod
    def get_server_by_uuid(self, server_id):
        pass

    @abc.abstractmethod
    def get_server_by_name(self, server_name):
        pass

    @abc.abstractmethod
    def update_server(self, server_uuid, **kwargs):
        pass

    @abc.abstractmethod
    def reserve_server(self, server_instance):
        pass

    @abc.abstractmethod
    def cancel_reservation(self, server_uuid):
        pass

    @abc.abstractmethod
    def deploy_server(self, server_uuid, *args, **kwargs):
        pass

    @abc.abstractmethod
    def return_server_to_pool(self, server_id, *args, **kwargs):
        pass
