# -*- encoding: utf-8 -*-

"""Pecan request hooks."""

from pecan import hooks
from ironic_inventory.db import api as dbapi


class SqlAlchemyHook(hooks.PecanHook):

    def before(self, state):
        state.request.dbapi = dbapi.get_instance()
