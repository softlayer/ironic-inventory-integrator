# -*- encoding: utf-8 -*-

"""API/Interface to the SQLAlchemy backend.
"""
import copy
from oslo_config import cfg
from oslo_db import exception as db_exc
from oslo_db.sqlalchemy import session as db_session
from oslo_log import log
from sqlalchemy.orm import exc as sqla_exc

from ironic_inventory.common import exceptions
from ironic_inventory.db import api
from ironic_inventory.db.sqlalchemy import models

CONF = cfg.CONF
LOG = log.getLogger(__name__)
_FACADE = None


def _create_facade_lazily():
    global _FACADE
    if _FACADE is None:
        _FACADE = db_session.EngineFacade.from_config(CONF)
    return _FACADE


def get_engine():
    facade = _create_facade_lazily()
    return facade.get_engine()


def get_session(**kwargs):
    facade = _create_facade_lazily()
    return facade.get_session(**kwargs)

def get_backend():
    """

    :return:
    """
    return Connection()


class Connection(api.Connection):

    def __init__(self):
        pass

    def _get_servers_query(self, kwargs):
        session = get_session()
        filters = copy.copy(kwargs)
        filters['reservation_id'] = None
        filters['deployed'] = False
        query = session.query(models.Server).filter_by(**filters)
        return query


    def _delete_reservation(self, reservation_id, server_uuid):
        session = get_session()
        with session.begin():
            query = session.query(models.Reservation).filter_by(id=reservation_id)
            try:
                reservation = query.one()
            except sqla_exc.NoResultFound:
                # HACK(caustin): For now, swallow this exception.
                # in the very near future roll back the deployment of the
                # server raise and error .
                LOG.warn('Reservation for server being %(uuid)s deployed was not'
                         'found.', {'uuid': server_uuid})

            session.delete(reservation)


    def add_server(self, **kwargs):
        """Adds a provisional server to the inventory.

        :param name: The Server's name or id.
        :param cpu_count: The number of CPUs in the server.
        :param chassis_drive_capacity: The drive capacity of the server's chassis.
        :param psu_capacity: The server's power supply capicity.
        :param chassis_size: The size of the server's chassis.
        :param memory: The server's memory in MB.
        :param local_drive_size: The size in GB of the local drive.
        :param driver_name: The name of the Ironic provisioning driver.
        :param deploy_kernel: The UUID of the deploy kernel.
        :param deploy_ramdisk: The UUID of the deploy ramdisk.
        :param ipmi_address: The IP Address of the IPMI interface.
        :param ipmi_password: The Password for the IPMI user.
        :param impi_username: The User ID / name of the IPMI user.
        :param impi_priv_level: The IPMI Privilege Level of the user.
        :param ipmi_mac_address: The MAC Address of the IPMI interface.
        :param cpu_arch: The CPU Architecture.  Defaults to 'x86_64'
        """

        server = models.Server()
        server.update(kwargs)
        try:
            server.save()
        except db_exc.DBDuplicateEntry as exc:
            if 'ipmi_mac_address' in exc.columns:
                raise exceptions.ExistingMACAddress(
                    address=kwargs['ipmi_mac_address'])
            if 'name' in exc.columns:
                raise exceptions.ExistingServerName(name=kwargs['name'])
            else:
                raise exceptions.ExistingServer()

        return server


    def remove_server(self, uuid):
        """Remove a server from the inventory pool.

        :param uuid: The server's uuid.
        """
        session = get_session()
        with session.begin():
            query = session.query(models.Server).filter_by(uuid=uuid)

            try:
                server = query.one()
            except sqla_exc.NoResultFound:
                raise exceptions.ServerNotFound(server_uuid=uuid)

            if server.reservation_id:
                # Don't delete servers with an existing reservation.
                raise exceptions.ServerReserved()

            query.delete()


    def get_all_servers(self):
        """Get all servers as a list.
        """

        session = get_session()
        return session.query(models.Server).all()


    def get_matching_servers(self, **kwargs):
        """Return a list of servers that match the search parameters.

        :param cpu_count: The number of CPUs in the server.
        :param chassis_drive_capacity: The drive capacity of the server's chassis.
        :param psu_capacity: The server's power supply capicity.
        :param chassis_size: The size of the server's chassis.
        :param memory: The server's memory in MB.
        :param local_drive_size: The size in GB of the local drive.
        :param cpu_arch: The CPU Architecture.  Defaults to 'x86_64'

        :return: list
        """

        try:
            query = self._get_servers_query(kwargs)
            servers = query.all()
            for server in servers:
                self.reserve_server(server)

        except sqla_exc.NoResultFound:
            # Note(caustin): For now, I am considering the case where no match is
            # found to not be an exception. So, just return None.
            return None

        return servers


    def get_single_server_match(self, **kwargs):
        """Return a single server that matches the search parameters.

        :param cpu_count: The number of CPUs in the server.
        :param chassis_drive_capacity: The drive capacity of the server's chassis.
        :param psu_capacity: The server's power supply capicity.
        :param chassis_size: The size of the server's chassis.
        :param memory: The server's memory in MB.
        :param local_drive_size: The size in GB of the local drive.
        :param cpu_arch: The CPU Architecture.  Defaults to 'x86_64'
        """

        try:
            query = self._get_servers_query(kwargs)
            server = query.first()
            self.reserve_server(server)

        except sqla_exc.NoResultFound:
            # Note(caustin): For now, I consider the case where no server meeting
            # the critera is found to be non-exceptional.  So, returning None in
            # this case.
            return None

        return server


    def get_server_by_uuid(self, server_id):
        """Get a server by it's uuid
        :param server_id:  The server's uuid
        """

        session = get_session()
        query = session.query(models.Server).filter_by(uuid=server_id)
        try:
            return query.one()
        except sqla_exc.NoResultFound:
            raise exceptions.ServerNotFound(uuid=server_id)


    def get_server_by_name(self, server_name):
        """Get a server by it's name.

        :param server_name: The server's unique name.
        """
        session = get_session()
        query = session.query(models.Server).filter_by(name=server_name)
        try:
            return query.one()
        except sqla_exc.NoResultFound:
            raise exceptions.ServerNotFound(name=server_name)


    def update_server(self, server_uuid, **kwargs):
        """

        :param server_uuid:
        :param kwargs:
        """
        session = get_session()
        with session.begin():
            query = session.query(models.Server).filter_by(uuid=server_uuid)
            try:
                # TODO (caustin): 'with_lockmode' has been superseded by
                # with_for_update in SQLAlchemy.  Update and test when possible.
                server = query.with_lockmode('update').one()
            except sqla_exc.NoResultFound:
                raise exceptions.ServerNotFound(uuid=server_uuid)

            if server.reservation_id:
                # We probably shouldn't update a server that has an existing
                # reservation in place.
                raise exceptions.ServerReserved()

            server.update(kwargs)
        return server


    def reserve_server(self, server_instance):
        """Create a reservation for a server.

        :param server_instance: A server object.
        """

        if server_instance.reservation_id:
            raise exceptions.ServerReserved(server_uuid=server_instance.uuid)

        reservation = models.Reservation()
        reservation.save()
        server_instance.update({'reservation_id': reservation.id})
        server_instance.save()

        return server_instance


    def cancel_reservation(self, server_uuid):
        """Cancel a reservation for a server.
        """

        server = self.get_server_by_uuid(self, server_uuid)
        reservation_id = server.reservation_id

        if not reservation_id:
            raise exceptions.ServerNotReserved(self, server_uuid=server_uuid)

        updated_server = self.update_server(self, server_uuid, **{'reservation_id': None})
        self._delete_reservation(server.reservation_id, server_uuid)

        return updated_server


    def deploy_server(self, server_uuid, *args, **kwargs):
        """Mark a server as being used by an ironic node.

        :param server_instance:
        :param args:
        :param kwargs:
        :return:
        """

        server = self.get_server_by_uuid(server_uuid)
        reservation_id = server.reservation_id

        if reservation_id:
            raise exceptions.ServerNotReserved(server_uuid)

        update_values = {'reservation_id': None, 'deployed': True}
        deployed_server = self.update_server(server_uuid, **update_values)
        self._delete_reservation(reservation_id, server_uuid)

        return deployed_server


    def return_server_to_pool(self, server_uuid, *args, **kwargs):
        """Returns a previously deployed server to the pool of available servers.

        :param server_uuid:
        :param args:
        :param kwargs:
        :return:
        """

        session = get_session()
        with session.begin():
            query = session.query(models.Server).filter_by(uuid=server_uuid)
            try:
                server = query.with_lockmode('update').one()
            except sqla_exc.NoResultFound:
                raise exceptions.ServerNotFound(uuid=server_uuid)

            if not server.deployed:
                raise exceptions.ServerNotDeployed(uuid=server_uuid)

            server.update({'deployed': False})
        return server
