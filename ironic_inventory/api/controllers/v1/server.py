# -*- encoding: utf-8 -*-


import pecan
from pecan import rest
from wsme import types as wtypes

from ironic_inventory.api.controllers.base import ApiBase
from ironic_inventory.api.controllers.root import wsme_expose
from ironic_inventory.db import api as dbapi
from ironic_inventory.objects.server import ServerFields


class Server(ApiBase):
    """API Representation of a Server.

    """

    id = wtypes.StringType
    uuid = wtypes.StringType
    name = wtypes.StringType
    cpu_count = wtypes.IntegerType
    local_drive_capacity = wtypes.IntegerType
    psu_capacity = wtypes.IntegerType
    psu_size = wtypes.IntegerType
    memory_mb = wtypes.IntegerType
    cpu_architecture = wtypes.StringType
    ipmi_password = wtypes.StringType
    ipmi_username = wtypes.StringType
    ipmi_priv_level = wtypes.StringType
    ipmi_mac_address = wtypes.StringType
    reservation_id = wtypes.StringType
    deployed = wtypes.BinaryType

    def __init__(self, **kwargs):
        self.fields = []
        for field in ServerFields:
            if not hasattr(self, field):
                continue
            self.fields.append(field)
            setattr(self, field, kwargs.get(field, wtypes.Unset))


    @classmethod
    def from_dict(cls, **kwargs):
        server = cls(
            id=kwargs.get('id'),
            uuid=kwargs.get('uuid'),
            name=kwargs.get('name'),
            cpu_count=kwargs.get('cpu_count'),
            local_drive_capacity=kwargs.get('local_drive_capacity'),
            psu_capacity=kwargs.get('psu_capacity'),
            psu_size=kwargs.get('psu_size'),
            memory_mb=kwargs.get('memory_mb'),
            cpu_architecture=kwargs.get('cpu_architecture'),
            ipmi_password=kwargs.get('ipmi_password'),
            ipmi_username=kwargs.get('ipmi_username'),
            ipmi_priv_level=kwargs.get('ipmi_priv_level'),
            ipmi_mac_address=kwargs.get('ipmi_mac_address'),
            reservation_id=kwargs.get('reservation_id'),
            deployed=kwargs.get('deployed')
        )
        return server


class ServerCollection(ApiBase):

    servers = [Server]

    @classmethod
    def from_list_of_dicts(cls, server_list):
        """

        :param server_list:
        :return:
        """

        collection = cls()
        collection.servers = [
            Server.from_dict(server.as_dict) for server in server_list]

        return collection


class ServerController(rest.RestController):

    dbapi = dbapi.get_instance()

    @wsme_expose(Server, wtypes.StringType)
    def get_one(self, server_uuid):
        """Get a single server.

        :return:
        """

        server = Server.from_dict(
            self.dbapi.get_server_by_uuid(server_uuid).as_dict())
        return server

    @wsme_expose(ServerCollection, wtypes.StringType, int, wtypes.text, wtypes.text)
    def get_all(self):

        servers = self.dbapi.get_all_servers()
        return ServerCollection.from_list_of_dicts(servers)

    @wsme_expose(Server, body=Server, status_code=201)
    def post(self, server):
        """Create a new server.

        :param server: A server supplied via the request body.
        """

        db_server = self.dbapi.add_server(pecan.request.contex, **server.as_dict())
        return Server.from_dict(db_server.as_dict())



