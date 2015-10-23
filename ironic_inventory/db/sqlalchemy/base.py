# -*- encoding: utf-8 -*-

"""Base definitions for SQLAlchemy and db specific configurations."""

from oslo_config import cfg
from oslo_db import options as db_options
from oslo_db.sqlalchemy import models as oslo_models
from sqlalchemy.ext.declarative import declarative_base
from ironic_inventory.common import paths

sql_opts = [
    cfg.StrOpt('mysql_engine',
               default='InnoDB',
               help='MySQL engine to use.')
]

_DEFAULT_SQL_CONNECTION = 'sqlite:///' + paths.state_path_def('inventory.sqlite')
db_options.set_defaults(cfg.CONF, _DEFAULT_SQL_CONNECTION, 'ironic.sqlite')


class InventoryBase(oslo_models.TimestampMixin, oslo_models.ModelBase):
    """DeclarativeBaseImpl class for inventory objects. """

    def as_dict(self):
        """Represent a SQLAlchemy declarative base model as a dict by
        introspecting it's columns.
        """

        # Note(caustin): A dict. comprehension may be better here but, it is
        # unclear if the case of a empty table needs to be considered.
        model_dict = dict()

        for colum in self.__table__.columns:
            model_dict[colum.name] = self[colum.name]

        return model_dict

    def save(self, session=None):
        """Override ModelBase.save() to handle the case of session=None"""

        # Note(caustin): This may be indicative of a smell from the project's
        # layout. Look at refactoring the internal API to avoid this.
        import ironic_inventory.db.sqlalchemy.api as db_api

        if session is None:
            session = db_api.get_session()

        super(InventoryBase, self).save(session)


DeclarativeBaseImpl = declarative_base(cls=InventoryBase)
