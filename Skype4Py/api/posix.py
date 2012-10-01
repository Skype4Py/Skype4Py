"""
Low level *Skype for Linux* interface.

This module handles the options that you can pass to `Skype.__init__` for Linux machines.
The options include:

- ``Transport`` (str) - Name of a channel used to communicate with the Skype client.
  Currently supported values:
  
  - ``'dbus'`` (default)

    Uses *DBus* thrugh *dbus-python* package.
    This is the default if no transport is specified.

    Look into `Skype4Py.api.posix_dbus` for additional options.

  - ``'x11'``

    Uses *X11* messaging through *Xlib*.

    Look into `Skype4Py.api.posix_x11` module for additional options.
"""
__docformat__ = 'restructuredtext en'


from Skype4Py.errors import SkypeAPIError


__all__ = ['SkypeAPI']


def SkypeAPI(opts):
    trans = opts.pop('Transport', 'dbus')
    if trans == 'dbus':
        from posix_dbus import SkypeAPI
    elif trans == 'x11':
        from posix_x11 import SkypeAPI
    else:
        raise SkypeAPIError('Unknown transport: %s' % trans)
    return SkypeAPI(opts)
