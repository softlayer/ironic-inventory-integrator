from pecan import rest
from wsme import types as wtpes

from ironic_inventory.api.controllers.base import ApiBase


class Reservation(ApiBase):
    """API repersentation of a  reservation."""

    id = wtpes.IntegerType
