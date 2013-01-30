"""
Skype4Py is a multiplatform Skype API wrapper for Python.
"""
__docformat__ = 'restructuredtext en'


from skype import Skype
from callchannel import CallChannelManager
from errors import SkypeError, SkypeAPIError
from enums import *
from api import platform
import logging


"""The version of Skype4Py."""


class NullHandler(logging.Handler):
    def emit(self, record):
        pass


# Suppress the "No handlers could be found for logger (...)" message.
logging.getLogger('Skype4Py').addHandler(NullHandler())
