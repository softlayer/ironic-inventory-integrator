# -*- encoding: utf-8 -*-

import sys
from oslo_config import cfg

# from ironic_inventory.common import service
# from ironic_inventory.db import migration

CONF = cfg.CONF

class DBCommand(object):
    pass


def main():
    valid_commands = {
        'upgrade', 'downgrade', 'revision', 'version', 'stamp',
        'create_schema'
    }

    service.prepare_service(sys.argv)
    CONF.command.func()
