# -*- encoding: utf-8 -*-

"""
Root controller for web api.
"""

from pecan import rest
from wsme import types as wtpes

from ironic_inventory.api.controllers.base import wsme_expose


class Version(object):

    """The version's ID"""
    id = wtpes.text

    @staticmethod
    def get_default(id):
        version = Version()
        version.id = id
        return version


class Root(object):
    """The name of the API"""
    name = wtpes.text

    """The suported versions"""
    versions = [Version]

    """The default version"""
    default_version = Version

    @staticmethod
    def get_default():
        """

        :return:
        """
        version_one = Version.get_default('v1')

        root = Root()
        root.name = "Ironic Inventory Manager"
        root.versions = [version_one]
        root.default_version = version_one

        return root

class RootController(rest.RestController):

    @wsme_expose(Root)
    def get(self):
        return Root.get_default()
