# -*- encoding: utf-8 -*-

from pecan import rest
from wsme import types as wtypes

from ironic_inventory.api.controllers.root import wsme_expose
from ironic_inventory.db.sqlalchemy.api import Connection


class ApiBase(wtypes.Base):
    """A Base Object for handling serialization of objects from request
    """

    def as_dict(self):
        return {key: getattr(self, key) for key in self.fields}


class Server(ApiBase):

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

    connection = Connection()

    @wsme_expose(Server, wtypes.StringType)
    def get_one(self, server_uuid):
        """Get a single server.

        :return:
        """

        server = Server.from_dict(
            self.connection.get_server_by_uuid(server_uuid).as_dict())
        return server

    @wsme_expose(ServerCollection, wtypes.StringType, int, wtypes.text, wtypes.text)
    def get_all(self):

        servers = self.connection.get_all_servers()
        return ServerCollection.from_list_of_dicts(servers)

    @wsme_expose(Server, body=Server, status_code=201)
    def post(self, server):

        pass
