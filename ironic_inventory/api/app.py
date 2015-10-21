import pecan
from pecan import make_app

from ironic_inventory.api import config


def get_pecan_config():
    """Load the pecan configuration file and return the config object"""

    config_file = config.__file__.replace('.pyc', '.py')
    return pecan.configuration.conf_from_file(config_file)

def setup_app(config):

    pecan_config = get_pecan_config()
    app = make_app(
        pecan_config.app.root,
        static_root=pecan_config.app.static_root,
        debug=pecan_config.app.debug,
        force_canonical=getattr(pecan_config.app, 'force_canonical', True),
    )

    return app
