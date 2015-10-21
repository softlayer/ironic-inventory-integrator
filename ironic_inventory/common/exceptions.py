# -*- encoding: utf-8 -*-

"""Common exceptions for the inventory manager.
"""


class ExistingMACAddress(Exception):
    code = 409
    message = u'A server with the MAC address %(address)s already exists.'

    def __init__(self, address, message=None,  **kwargs):
        """
        :param address: The conflicting MAC address.
        :param message: The exception message. Optional
        """

        if not message:
            # Construct the default message.
            message = self.message % address

        super(ExistingMACAddress, self).__init__(message)


class ExistingServerName(Exception):
    code = 409
    message = u'A server using the name %(name)s already exists.'

    def __init__(self, name, message=None, **kwargs):
        """
        :param name:
        :param message:
        :param kwargs:
        """

        if not message:
            message = self.message % name

        super(ExistingServerName, self).__init__(message)


class ExistingServer(Exception):
    code = 409
    message = u'This server already exists.'

    def __init__(self):
        super(ExistingServer, self).__init__()


class ServerNotFound(Exception):
    code = 404
    message = u'The server %(identifier)s was not found.'

    def __init__(self, message=None, **kwargs):
        """
        :param message: An overridden exception message.
        :param uuid: The server's uuid
        :param name: The server's name
        """

        if not message:
            if kwargs.get('name'):
                message = self.message % kwargs['name']
            elif kwargs.get('uuid'):
                message = self.message % kwargs['uuid']
            else:
                message = u'The server was not found.'

        super(ServerNotFound, self).__init__(message)


class ServerReserved(Exception):
    message = ('The server %(uuid) has an existing reservation, please remove'
               ' the reservation and retry.')

    def __init__(self, message=None, **kwargs):
        """
        :param message:
        :param server_uuid:
        """

        if not message:
            uuid = kwargs.get('server_uuid')
            if not uuid:
                message = ('The server has an existing reservation, please'
                           ' remove and retry the operation.')
            else:
                message = self.message % uuid

        super(ServerReserved, self).__init__(message)


class ServerNotReserved(Exception):
    message = 'The server %(server_uuid)s does not have a reservation.'

    def __init__(self, message=None, **kwargs):

        if not message:
            uuid = kwargs.get('server_uuid')
            if not uuid:
                message = 'The server does not have an existing reservation.'
            else:
                message = self.message % uuid

        super(ServerNotReserved, self).__init__(message)


class ServerNotDeployed(Exception):
    message = 'The server %(uuid)s is not in a deployed state.'

    def __init__(self, message=None, **kwargs):
        """
        :param message: A custom message.
        :param uuid: The server's uuid
        """

        if not message:
            uuid = kwargs.get('uuid')
            if not uuid:
                message = 'The server is not in a deployed state.'
            else:
                message = self.message % uuid

        super(ServerNotDeployed, self).__init__(message)
