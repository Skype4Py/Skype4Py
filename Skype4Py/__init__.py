"""
Skype4Py is a multiplatform Skype API wrapper for Python.

Usage
=====

   Everything that you should ever need is available as aliases in the ``Skype4Py`` package.
   Import it using the standard form of the ``import`` statement:
   
   .. python::
   
     import Skype4Py
     
   Importing the whole package into your script's namespace using ``from Skype4Py import *`` is
   generally discouraged. You should also not access the modules in the package directly as they
   are considered an implementation detail and may change in future versions without notice.
   
   The package provides the following:

   - Classes  
     
     ``Skype4Py.Skype``, an alias for `Skype4Py.skype.Skype`
     
     ``Skype4Py.CallChannelManager``, an alias for `Skype4Py.callchannel.CallChannelManager`
     
   - Constants
     
     Everything from the `Skype4Py.enums` module.

     ``platform``, either ``'windows'``, ``'posix'`` or ``'darwin'`` depending
     on the current platform (Windows, Linux, Mac OS X).
     
   - Errors
   
     ``Skype4Py.SkypeError``, an alias for `Skype4Py.errors.SkypeError`
     
     ``Skype4Py.SkypeAPIError``, an alias for `Skype4Py.errors.SkypeAPIError`

   The two classes exposed by the ``Skype4Py`` package are the only ones that are to be instantiated
   directly. They in turn provide means of instantiating the remaining ones. They are also the only
   classes that provide event handlers (for more information about events and how to use them, see
   the `EventHandlingBase` class.
   
   Every Skype4Py script instantiates at least the ``Skype4Py.Skype`` class which gives access to
   the Skype client running currently in the system. Follow the `Skype4Py.skype.Skype` reference to
   see what you can do with it.

   **Warning!** While reading this documentation, it is important to keep in mind that everything
   needed is in the top package level because the documentation refers to all objects in the places
   they actually live.

Quick example
=============

   This short example connects to Skype client and prints the user's full name and the names of all the
   contacts from the contacts list:

   .. python::

       import Skype4Py

       # Create an instance of the Skype class.
       skype = Skype4Py.Skype()

       # Connect the Skype object to the Skype client.
       skype.Attach()

       # Obtain some information from the client and print it out.
       print 'Your full name:', skype.CurrentUser.FullName
       print 'Your contacts:'
       for user in skype.Friends:
           print '    ', user.FullName

Note on the naming convention
=============================

   Skype4Py uses two different naming conventions. The first one applies to interfaces derived from
   Skype4COM_, a COM library which was an inspiration for Skype4Py. This convention uses the ``CapCase``
   scheme for class names, properties, methods and their arguments. The constants use the ``mixedCase``
   scheme.
   
   The second naming convention is more "Pythonic" and is used by all other parts of the package
   including internal objects. It uses mostly the same ``CapCase`` scheme for class names (including
   exception names) with a small difference in abbreviations. Where the first convention would use
   a ``SkypeApiError`` name, the second one uses ``SkypeAPIError``. Other names including properties,
   methods, arguments, variables and module names use lowercase letters with underscores.

.. _Skype4COM: https://developer.skype.com/Docs/Skype4COM
.. |copy| unicode:: U+000A9

:author: Arkadiusz Wahlig <arkadiusz.wahlig@gmail.com>
:requires: Python 2.4 up until but not including 3.0.
:see: The Skype4Py website: https://developer.skype.com/wiki/Skype4Py
:license: BSD License (see the accompanying LICENSE file for more information)
:copyright: |copy| 2007-2009 Arkadiusz Wahlig
"""
__docformat__ = 'restructuredtext en'


from skype import Skype
from callchannel import CallChannelManager
from errors import SkypeError, SkypeAPIError
from enums import *
from api import platform
import logging


__version__ = '1.0.32.0'
"""The version of Skype4Py."""


class NullHandler(logging.Handler):
    def emit(self, record):
        pass


# Suppress the "No handlers could be found for logger (...)" message.
logging.getLogger('Skype4Py').addHandler(NullHandler())
