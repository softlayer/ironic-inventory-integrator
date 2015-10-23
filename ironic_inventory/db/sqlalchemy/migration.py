# -*- encoding: utf-8 -*-

"""Database setup and migration commands."""

from oslo_config import cfg
from stevedore import driver

_IMPL = None


def get_backend():
    global _IMPL
    if not _IMPL:
        cfg.CONF.import_opt('backend', 'oslo_db.options', group='database')
        _IMPL = driver.DriverManager("ironic_inventory.database.migration_backend",
                                     cfg.CONF.database.backend).driver
    return _IMPL


def upgrade(version=None):
    """Migrate the database to `version` or the most recent version."""
    return get_backend().upgrade(version)


def downgrade(version=None):
    return get_backend().downgrade(version)


def version():
    return get_backend().version()


def stamp(version):
    return get_backend().stamp(version)


def revision(message, autogenerate):
    return get_backend().revision(message, autogenerate)


def create_schema():
    return get_backend().create_schema()

