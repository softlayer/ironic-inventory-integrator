# -*- encoding: utf-8 -*-

"""Database API for CRUD on inventory servers.
"""

from oslo_config import cfg
from oslo_db import api as db_api


_BACKEND_MAPPING = {'sqlalchemy': 'ironic_inventory.db.sqlalchemy.api'}
IMPL = db_api.DBAPI.from_config(cfg.CONF, backend_mapping=_BACKEND_MAPPING)


def get_instance():
    return IMPL

