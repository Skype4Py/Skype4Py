"""
Low-level Skype API definitions.

This subpackage imports one of the:

- `Skype4Py.api.darwin`
- `Skype4Py.api.posix`
- `Skype4Py.api.windows`

modules based on the current platform.

Name of the imported module in available in the `platform` variable.

The modules implement the low-level Skype API and define options
for the `Skype.__init__` constructor.
"""
__docformat__ = 'restructuredtext en'


import sys
import threading
import logging

from Skype4Py.utils import *
from Skype4Py.enums import apiAttachUnknown
from Skype4Py.errors import SkypeAPIError


__all__ = ['Command', 'SkypeAPINotifier', 'SkypeAPI']


DEFAULT_PROTOCOL = 5
DEFAULT_FRIENDLYNAME = u'Skype4Py'
DEFAULT_TIMEOUT = 30000


class Command(object):
    """Represents an API command. Use `Skype.Command` to instantiate.

    To send a command to Skype, use `Skype.SendCommand`.
    """

    def __init__(self, Command, Expected=u'', Blocking=False, Timeout=DEFAULT_TIMEOUT, Id=-1):
        """Use `Skype.Command` to instantiate the object instead of doing it directly.
        """

        self.Blocking = Blocking
        """If set to True, `Skype.SendCommand` will block until the reply is received.
        
        :type: bool"""

        self.Command = tounicode(Command)
        """Command string.
        
        :type: unicode"""

        self.Expected = tounicode(Expected)
        """Expected reply.
        
        :type: unicode"""

        self.Id = Id
        """Command Id.
        
        :type: int"""

        self.Reply = u''
        """Reply after the command has been sent and Skype has replied.
        
        :type: unicode"""

        self.Timeout = Timeout
        """Timeout if Blocking == True.
        
        :type: int"""

    def __repr__(self):
        return '<%s with Command=%s, Blocking=%s, Reply=%s, Id=%s>' % \
            (object.__repr__(self)[1:-1], repr(self.Command), self.Blocking, repr(self.Reply), self.Id)

    def timeout2float(self):
        """A wrapper for `api.timeout2float` function. Returns the converted
        `Timeout` property.
        """
        return timeout2float(self.Timeout)


class SkypeAPINotifier(object):
    def attachment_changed(self, status):
        pass

    def notification_received(self, notification):
        pass
        
    def sending_command(self, command):
        pass

    def reply_received(self, command):
        pass


class SkypeAPIBase(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name='Skype4Py API thread')
        self.setDaemon(True)
        if not hasattr(self, 'logger'):
            # Create a logger if the subclass hasn't done it already.
            self.logger = logging.getLogger('Skype4Py.api.SkypeAPIBase')
        self.friendly_name = DEFAULT_FRIENDLYNAME
        self.protocol = DEFAULT_PROTOCOL
        self.commands = {}
        # This lock is the main mechanism to make Skype4Py thread-safe.
        self.rlock = threading.RLock()
        self.notifier = SkypeAPINotifier()
        self.attachment_status = apiAttachUnknown
        self.logger.info('opened')

    def _not_implemented(self):
        raise SkypeAPIError('Function not implemented')
        
    def set_notifier(self, notifier):
        self.notifier = notifier
        
    def push_command(self, command):
        self.acquire()
        try:
            if command.Id < 0:
                command.Id = 0
                while command.Id in self.commands:
                    command.Id += 1
            elif command.Id in self.commands:
                raise SkypeAPIError('Command Id conflict')
            self.commands[command.Id] = command
        finally:
            self.release()

    def pop_command(self, id_):
        self.acquire()
        try:
            try:
                return self.commands.pop(id_)
            except KeyError:
                return None
        finally:
            self.release()

    def acquire(self):
        self.rlock.acquire()
        
    def release(self):
        self.rlock.release()

    def close(self):
        self.logger.info('closed')

    def set_friendly_name(self, friendly_name):
        self.friendly_name = friendly_name

    def set_attachment_status(self, attachment_status):
        if attachment_status != self.attachment_status:
            self.logger.info('attachment: %s', attachment_status)
            self.attachment_status = attachment_status
            self.notifier.attachment_changed(attachment_status)

    def attach(self, timeout, wait=True):
        self._not_implemented()

    def is_running(self):
        self._not_implemented()

    def startup(self, minimized, nosplash):
        self._not_implemented()

    def shutdown(self):
        self._not_implemented()

    def send_command(self, command):
        self._not_implemented()

    def security_context_enabled(self, context):
        self._not_implemented()

    def enable_security_context(self, context):
        self._not_implemented()

    def allow_focus(self, timeout):
        pass


def timeout2float(timeout):
    """Converts a timeout expressed in milliseconds or seconds into a timeout expressed
    in seconds using a floating point number.
    
    :Parameters:
      timeout : int, long or float
        The input timeout. Assumed to be expressed in number of
        milliseconds if the type is int or long. For float, assumed
        to be a number of seconds (or fractions thereof).
    
    :return: The timeout expressed in number of seconds (or fractions thereof).
    :rtype: float
    """
    if isinstance(timeout, float):
        return timeout
    return timeout / 1000.0


def finalize_opts(opts):
    """Convinient function called after popping all options from a dictionary.
    If there are any items left, a TypeError exception is raised listing all
    unexpected keys in the error message.
    """
    if opts:
        raise TypeError('Unexpected option(s): %s' % ', '.join(opts.keys()))


# Select appropriate low-level Skype API module
if getattr(sys, 'skype4py_setup', False):
    # dummy for the setup.py run
    SkypeAPI = lambda **Options: None
    platform = ''
elif sys.platform.startswith('win'):
    from windows import SkypeAPI
    platform = 'windows'
elif sys.platform == 'darwin':
    from darwin import SkypeAPI
    platform = 'darwin'
else:
    from posix import SkypeAPI
    platform = 'posix'


# Note. py2exe will include the darwin but not the posix module. This seems to be the case
# solely because of the "posix" name. It might be a bug in py2exe or modulefinder caused
# by a failed attempt to import a "posix" module by the os module. If this is encountered
# during modulefinder scanning, the Skype4Py.api.posix is simply ignored.
#
# That being said ideally we would like to exclude both of them but I couldn't find a way
# to cause py2exe to skip them. I think py2exe should expose mechanisms to cooperate with
# extension modules aware of its existence.
