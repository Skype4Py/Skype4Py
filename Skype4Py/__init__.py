"""
Skype4Py is a multiplatform Skype API wrapper for Python.
"""
__docformat__ = 'restructuredtext en'

import sys

is_64bits = sys.maxsize > 2**32

if is_64bits and sys.platform == "darwin":
    raise RuntimeError("Skype4Py currently works only on 32-bit architecture. On 64-bit platforms you need to run this application in 32-bit compatibility mode. Please see documentation and Github issue tracker for more details.")


from skype import Skype
from callchannel import CallChannelManager
from errors import SkypeError, SkypeAPIError
from enums import *
from api import platform
import logging


class NullHandler(logging.Handler):
    def emit(self, record):
        pass


# Suppress the "No handlers could be found for logger (...)" message.
logging.getLogger('Skype4Py').addHandler(NullHandler())
