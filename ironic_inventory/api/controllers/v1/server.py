# -*- encoding: utf-8 -*-

from wsme import types as wtypes

class Collection(object):

    next = wtypes.text

    @property
    def collection(self):
        return None
        # server["chassis_drive_capacity"] = extra_specs.get('inventory:chassis_drive_capacity', None)
        # server["chassis_psu_capacity"] = extra_specs.get('inventory:chassis_psu_capacity', None)
        # server["chassis_size"] = extra_specs.get('inventory:chassis_size', None)
        # server["cpu_core_count"] = extra_specs.get('inventory:cpu_core_count', None)
        # server["ram_capacity"] = extra_specs.get('inventory:ram_capacity', None)
        # server["active_components"] = []
        # proc_data = jsonutils.loads(extra_specs.get('inventory:proc_obj', None))
        # hdd_list = jsonutils.loads(extra_specs.get('inventory:hdd_list', []))


class Server(object):

    uuid = wtypes.StringType
    name = wtypes.StringType


class ServerCollection(object):


    servers = [Server]

    @property
    def collection(self):
        return None

