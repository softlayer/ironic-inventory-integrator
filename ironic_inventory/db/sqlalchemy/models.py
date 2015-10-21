# -*- encoding: utf-8 -*-

"""
SQLAlchemy models for bare metal inventory management.
"""

from sqlalchemy import Column, Integer, String, Boolean, schema
from sqlalchemy import ForeignKey, orm

from ironic_inventory.db.sqlalchemy.base import DeclarativeBaseImpl


class Server(DeclarativeBaseImpl):
    """Represents a Bare Metal Server."""

    # TODO(caustin): Look at this table and normalize.

    __tablename__ = 'servers'
    __table_args__ = (
        schema.UniqueConstraint('uuid', name='uniq_servers0uuid'),
        schema.UniqueConstraint('name', name='uniq_servers0name'),
        schema.UniqueConstraint('ipmi_mac_address',
                                name='uniq_servers0impmimacaddress'),)

    # server information.
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False)
    name = Column(String())
    cpu_count = Column(Integer())
    local_drive_capacity = Column(Integer())
    psu_capacity = Column(Integer())
    psu_size = Column(String(36))
    memory_mb = Column(Integer())
    cpu_architecture = Column(String(), default='x86_64')

    # Driver Information.
    driver_name = Column(String())
    deploy_kernel = Column(String())
    deploy_ramdisk = Column(String())

    # IPMI Information.
    ipmi_address = Column(String())
    ipmi_password = Column(String())
    impi_username = Column(String())
    impi_priv_level = Column(String(), default='OPERATOR')
    ipmi_mac_address = Column(String())

    # Reservation Data
    reservation_id = Column(Integer, ForeignKey('reservations.id'))
    reservation = orm.relationship('Reservation', uselist=False,
                                   cacade='all, delete-orphan',
                                   single_parent=True)
    # Deployed Flag
    # Note(caustin): This may be better normalized.
    deployed = Column(Boolean(), default=False)

class Reservation(DeclarativeBaseImpl):
    """Represents a reservation request for a server"""

    # Note(caustin): Using SQLAlchemy's method of declaring one-to-one
    # relationships.  This may be better suited as an association table if
    # there is the need for additional information to be stored in this table.

    __tablename__ = 'reservations'

    id = Column(Integer(), primary_key=True, autoincrement=True)

