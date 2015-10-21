# -*- encoding: utf-8 -*-

"""Common application path definitions and helper methods."""

import os

from oslo_config import cfg

path_opts = [
    cfg.StrOpt('pybasedir',
               default=os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                    '../')),
               help=('Directory where the ironic inventory python module is'
                     ' installed.')),
    cfg.StrOpt('bindir',
               default='$pybasedir/bin',
               help=('Directory where ironic inventory binaries are'
                    ' installed.')),
    cfg.StrOpt('state_path',
               default='$pybasedir',
               help=("Top-level directory for maintaining the invenotry"
                     " manager's state.")),
]

CONF = cfg.CONF
CONF.register_opts(path_opts)


def basedir_def(*args):
    """Return an uninterpolated path relative to $pybasedir."""
    return os.path.join('$pybasedir', *args)


def bindir_def(*args):
    """Return an uninterpolated path relative to $bindir."""
    return os.path.join('$bindir', *args)


def state_path_def(*args):
    """Return an uninterpolated path relative to $state_path."""
    return os.path.join('$state_path', *args)


def basedir_rel(*args):
    """Return a path relative to $pybasedir."""
    return os.path.join(CONF.pybasedir, *args)


def bindir_rel(*args):
    """Return a path relative to $bindir."""
    return os.path.join(CONF.bindir, *args)


def state_path_rel(*args):
    """Return a path relative to $state_path."""
    return os.path.join(CONF.state_path, *args)
