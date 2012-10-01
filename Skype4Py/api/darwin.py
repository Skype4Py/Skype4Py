"""
Low level *Skype for Mac OS X* interface implemented using *Carbon
distributed notifications*. Uses direct *Carbon*/*CoreFoundation*
calls through the *ctypes* module.

This module handles the options that you can pass to
`Skype.__init__` for *Mac OS X* machines.

- ``RunMainLoop`` (bool) - If set to False, Skype4Py won't start the Carbon event
  loop. Otherwise it is started in a separate thread. The loop must be running for
  Skype4Py events to work properly. Set this option to False if you plan to run the
  loop yourself or if, for example, your GUI framework does it for you.

Thanks to **Eion Robb** for reversing *Skype for Mac* API protocol.
"""
__docformat__ = 'restructuredtext en'


import sys
from ctypes import *
from ctypes.util import find_library
import threading
import time
import logging

from Skype4Py.api import Command, SkypeAPIBase, \
                         timeout2float, finalize_opts
from Skype4Py.errors import SkypeAPIError
from Skype4Py.enums import *


__all__ = ['SkypeAPI']


class CFType(object):
    """Fundamental type for all CoreFoundation types.

    :see: http://developer.apple.com/documentation/CoreFoundation/Reference/CFTypeRef/
    """

    def __init__(self, init):
        self.owner = True
        if isinstance(init, CFType):
            # copy the handle and increase the use count
            self.handle = init.get_handle()
            coref.CFRetain(self)
        elif isinstance(init, c_void_p):
            self.handle = init
        else:
            raise TypeError('illegal init type: %s' % type(init))

    @classmethod
    def from_handle(cls, handle):
        if isinstance(handle, (int, long)):
            handle = c_void_p(handle)
        elif not isinstance(handle, c_void_p):
            raise TypeError('illegal handle type: %s' % type(handle))
        obj = cls(handle)
        obj.owner = False
        return obj

    def __del__(self):
        if not coref:
            return
        if self.owner:
            coref.CFRelease(self)

    def __repr__(self):
        return '%s(handle=%s)' % (self.__class__.__name__, repr(self.handle))

    def retain(self):
        if not self.owner:
            coref.CFRetain(self)
            self.owner = True

    def get_retain_count(self):
        return coref.CFGetRetainCount(self)

    def get_handle(self):
        return self.handle

    # allows passing CF types as ctypes function parameters
    _as_parameter_ = property(get_handle)


class CFString(CFType):
    """CoreFoundation string type.

    Supports Python unicode type only. String is immutable.

    :see: http://developer.apple.com/documentation/CoreFoundation/Reference/CFStringRef/
    """

    def __init__(self, init=u''):
        if isinstance(init, (str, unicode)):
            s = unicode(init).encode('utf-8')
            init = c_void_p(coref.CFStringCreateWithBytes(None,
                                    s, len(s), 0x08000100, False))
        CFType.__init__(self, init)

    def __str__(self):
        i = coref.CFStringGetLength(self)
        size = c_long()
        if coref.CFStringGetBytes(self, 0, i, 0x08000100, 0, False, None, 0, byref(size)) > 0:
            buf = create_string_buffer(size.value)
            coref.CFStringGetBytes(self, 0, i, 0x08000100, 0, False, buf, size, None)
            return buf.value
        else:
            raise UnicodeError('CFStringGetBytes() failed')

    def __unicode__(self):
        return self.__str__().decode('utf-8')

    def __len__(self):
        return coref.CFStringGetLength(self)

    def __repr__(self):
        return 'CFString(%s)' % repr(unicode(self))


class CFNumber(CFType):
    """CoreFoundation number type.

    Supports Python int type only. Number is immutable.

    :see: http://developer.apple.com/documentation/CoreFoundation/Reference/CFNumberRef/
    """

    def __init__(self, init=0):
        if isinstance(init, (int, long)):
            init = c_void_p(coref.CFNumberCreate(None, 3, byref(c_int(int(init)))))
        CFType.__init__(self, init)

    def __int__(self):
        n = c_int()
        if coref.CFNumberGetValue(self, 3, byref(n)):
            return n.value
        return 0

    def __repr__(self):
        return 'CFNumber(%s)' % repr(int(self))


class CFDictionary(CFType):
    """CoreFoundation immutable dictionary type.

    :see: http://developer.apple.com/documentation/CoreFoundation/Reference/CFDictionaryRef/
    """

    def __init__(self, init={}):
        if isinstance(init, dict):
            d = dict(init)
            keys = (c_void_p * len(d))()
            values = (c_void_p * len(d))()
            for i, (k, v) in enumerate(d.items()):
                keys[i] = k.get_handle()
                values[i] = v.get_handle()
            init = c_void_p(coref.CFDictionaryCreate(None, keys, values, len(d),
                coref.kCFTypeDictionaryKeyCallBacks, coref.kCFTypeDictionaryValueCallBacks))
        CFType.__init__(self, init)

    def get_dict(self):
        n = len(self)
        keys = (c_void_p * n)()
        values = (c_void_p * n)()
        coref.CFDictionaryGetKeysAndValues(self, keys, values)
        d = dict()
        for i in xrange(n):
            d[CFType.from_handle(keys[i])] = CFType.from_handle(values[i])
        return d

    def __getitem__(self, key):
        return CFType.from_handle(coref.CFDictionaryGetValue(self, key))

    def __len__(self):
        return coref.CFDictionaryGetCount(self)


class CFDistributedNotificationCenter(CFType):
    """CoreFoundation distributed notification center type.

    :see: http://developer.apple.com/documentation/CoreFoundation/Reference/CFNotificationCenterRef/
    """

    CFNOTIFICATIONCALLBACK = CFUNCTYPE(None, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p)

    def __init__(self):
        CFType.__init__(self, c_void_p(coref.CFNotificationCenterGetDistributedCenter()))
        # there is only one distributed notification center per application
        self.owner = False
        self.callbacks = {}
        self._c_callback = self.CFNOTIFICATIONCALLBACK(self._callback)

    def _callback(self, center, observer, name, obj, userInfo):
        observer = CFString.from_handle(observer)
        name = CFString.from_handle(name)
        if obj:
            obj = CFString.from_handle(obj)
        userInfo = CFDictionary.from_handle(userInfo)
        callback = self.callbacks[(unicode(observer), unicode(name))]
        callback(self, observer, name, obj, userInfo)

    def add_observer(self, observer, callback, name=None, obj=None,
            drop=False, coalesce=False, hold=False, immediate=False):
        if not callable(callback):
            raise TypeError('callback must be callable')
        observer = CFString(observer)
        self.callbacks[(unicode(observer), unicode(name))] = callback
        if name is not None:
            name = CFString(name)
        if obj is not None:
            obj = CFString(obj)
        if drop:
            behaviour = 1
        elif coalesce:
            behaviour = 2
        elif hold:
            behaviour = 3
        elif immediate:
            behaviour = 4
        else:
            behaviour = 0
        coref.CFNotificationCenterAddObserver(self, observer,
                self._c_callback, name, obj, behaviour)

    def remove_observer(self, observer, name=None, obj=None):
        observer = CFString(observer)
        if name is not None:
            name = CFString(name)
        if obj is not None:
            obj = CFString(obj)
        coref.CFNotificationCenterRemoveObserver(self, observer, name, obj)
        try:
            del self.callbacks[(unicode(observer), unicode(name))]
        except KeyError:
            pass

    def post_notification(self, name, obj=None, userInfo=None, immediate=False):
        name = CFString(name)
        if obj is not None:
            obj = CFString(obj)
        if userInfo is not None:
            userInfo = CFDictionary(userInfo)
        coref.CFNotificationCenterPostNotification(self, name, obj, userInfo, immediate)


class EventLoop(object):
    """Carbon event loop object for the current thread.
    
    The Carbon reference documentation seems to be gone from developer.apple.com, the following
    link points to a mirror I found. I don't know how long until this one is gone too.
    
    :see: http://www.monen.nl/DevDoc/documentation/Carbon/Reference/Carbon_Event_Manager_Ref/index.html
    """
    
    def __init__(self):
        self.handle = c_void_p(carbon.GetCurrentEventLoop())

    @staticmethod
    def run(timeout=-1):
        # Timeout is expressed in seconds (float), -1 means forever.
        # Returns True if aborted (eventLoopQuitErr).
        return (carbon.RunCurrentEventLoop(timeout) == -9876)

    def stop(self):
        carbon.QuitEventLoop(self.handle)


# load the Carbon and CoreFoundation frameworks
# (only if not building the docs)
if not getattr(sys, 'skype4py_setup', False):

    path = find_library('Carbon')
    if path is None:
        raise ImportError('Could not find Carbon.framework')
    carbon = cdll.LoadLibrary(path)
    carbon.RunCurrentEventLoop.argtypes = (c_double,)

    path = find_library('CoreFoundation')
    if path is None:
        raise ImportError('Could not find CoreFoundation.framework')
    coref = cdll.LoadLibrary(path)


class SkypeAPI(SkypeAPIBase):
    """
    :note: Code based on Pidgin Skype Plugin source
           (http://code.google.com/p/skype4pidgin/).
           Permission to use granted by the author.
    """

    def __init__(self, opts):
        self.logger = logging.getLogger('Skype4Py.api.darwin.SkypeAPI')
        SkypeAPIBase.__init__(self)
        self.run_main_loop = opts.pop('RunMainLoop', True)
        finalize_opts(opts)
        self.center = CFDistributedNotificationCenter()
        self.is_available = False
        self.client_id = -1

    def run(self):
        self.logger.info('thread started')
        if self.run_main_loop:
            self.loop = EventLoop()
            EventLoop.run()
        self.logger.info('thread finished')

    def close(self):
        if hasattr(self, 'loop'):
            self.loop.stop()
            self.client_id = -1
        SkypeAPIBase.close(self)

    def set_friendly_name(self, friendly_name):
        SkypeAPIBase.set_friendly_name(self, friendly_name)
        if self.attachment_status == apiAttachSuccess:
            # reattach with the new name
            self.set_attachment_status(apiAttachUnknown)
            self.attach()

    def attach(self, timeout, wait=True):
        if self.attachment_status in (apiAttachPendingAuthorization, apiAttachSuccess):
            return
        self.acquire()
        try:
            try:
                self.start()
            except AssertionError:
                pass
            t = threading.Timer(timeout2float(timeout), lambda: setattr(self, 'wait', False))
            try:
                self.init_observer()
                self.client_id = -1
                self.set_attachment_status(apiAttachPendingAuthorization)
                self.post('SKSkypeAPIAttachRequest')
                self.wait = True
                if wait:
                    t.start()
                while self.wait and self.attachment_status == apiAttachPendingAuthorization:
                    if self.run_main_loop:
                        time.sleep(1.0)
                    else:
                        EventLoop.run(1.0)
            finally:
                t.cancel()
            if not self.wait:
                self.set_attachment_status(apiAttachUnknown)
                raise SkypeAPIError('Skype attach timeout')
        finally:
            self.release()
        command = Command('PROTOCOL %s' % self.protocol, Blocking=True)
        self.send_command(command)
        self.protocol = int(command.Reply.rsplit(None, 1)[-1])

    def is_running(self):
        try:
            self.start()
        except AssertionError:
            pass
        self.init_observer()
        self.is_available = False
        self.post('SKSkypeAPIAvailabilityRequest')
        time.sleep(1.0)
        return self.is_available

    def startup(self, minimized, nosplash):
        if not self.is_running():
            from subprocess import Popen
            nul = file('/dev/null')
            Popen(['/Applications/Skype.app/Contents/MacOS/Skype'], stdin=nul, stdout=nul, stderr=nul)

    def send_command(self, command):
        if not self.attachment_status == apiAttachSuccess:
            self.attach(command.Timeout)
        self.push_command(command)
        self.notifier.sending_command(command)
        cmd = u'#%d %s' % (command.Id, command.Command)
        if command.Blocking:
            if self.run_main_loop:
                command._event = event = threading.Event()
            else:
                command._loop = EventLoop()
        else:
            command._timer = timer = threading.Timer(command.timeout2float(), self.pop_command, (command.Id,))

        self.logger.debug('sending %s', repr(cmd))
        userInfo = CFDictionary({CFString('SKYPE_API_COMMAND'): CFString(cmd),
                                 CFString('SKYPE_API_CLIENT_ID'): CFNumber(self.client_id)})
        self.post('SKSkypeAPICommand', userInfo)

        if command.Blocking:
            if self.run_main_loop:
                event.wait(command.timeout2float())
                if not event.isSet():
                    raise SkypeAPIError('Skype command timeout')
            else:
                if not EventLoop.run(command.timeout2float()):
                    raise SkypeAPIError('Skype command timeout')
        else:
            timer.start()

    def init_observer(self):
        if self.has_observer():
            self.delete_observer()
        self.observer = CFString(self.friendly_name)
        self.center.add_observer(self.observer, self.SKSkypeAPINotification, 'SKSkypeAPINotification', immediate=True)
        self.center.add_observer(self.observer, self.SKSkypeWillQuit, 'SKSkypeWillQuit', immediate=True)
        self.center.add_observer(self.observer, self.SKSkypeBecameAvailable, 'SKSkypeBecameAvailable', immediate=True)
        self.center.add_observer(self.observer, self.SKAvailabilityUpdate, 'SKAvailabilityUpdate', immediate=True)
        self.center.add_observer(self.observer, self.SKSkypeAttachResponse, 'SKSkypeAttachResponse', immediate=True)

    def delete_observer(self):
        if not self.has_observer():
            return
        self.center.remove_observer(self.observer, 'SKSkypeAPINotification')
        self.center.remove_observer(self.observer, 'SKSkypeWillQuit')
        self.center.remove_observer(self.observer, 'SKSkypeBecameAvailable')
        self.center.remove_observer(self.observer, 'SKAvailabilityUpdate')
        self.center.remove_observer(self.observer, 'SKSkypeAttachResponse')
        del self.observer

    def has_observer(self):
        return hasattr(self, 'observer')

    def post(self, name, userInfo=None):
        if not self.has_observer():
            self.init_observer()
        self.center.post_notification(name, self.observer, userInfo, immediate=True)

    def SKSkypeAPINotification(self, center, observer, name, obj, userInfo):
        client_id = int(CFNumber(userInfo[CFString('SKYPE_API_CLIENT_ID')]))
        if client_id != 999 and (client_id == 0 or client_id != self.client_id):
            return
        cmd = unicode(CFString(userInfo[CFString('SKYPE_API_NOTIFICATION_STRING')]))
        self.logger.debug('received %s', repr(cmd))

        if cmd.startswith(u'#'):
            p = cmd.find(u' ')
            command = self.pop_command(int(cmd[1:p]))
            if command is not None:
                command.Reply = cmd[p + 1:]
                if command.Blocking:
                    if self.run_main_loop:
                        command._event.set()
                    else:
                        command._loop.stop()
                else:
                    command._timer.cancel()
                self.notifier.reply_received(command)
            else:
                self.notifier.notification_received(cmd[p + 1:])
        else:
            self.notifier.notification_received(cmd)

    def SKSkypeWillQuit(self, center, observer, name, obj, userInfo):
        self.logger.debug('received SKSkypeWillQuit')
        self.set_attachment_status(apiAttachNotAvailable)

    def SKSkypeBecameAvailable(self, center, observer, name, obj, userInfo):
        self.logger.debug('received SKSkypeBecameAvailable')
        self.set_attachment_status(apiAttachAvailable)

    def SKAvailabilityUpdate(self, center, observer, name, obj, userInfo):
        self.logger.debug('received SKAvailabilityUpdate')
        self.is_available = not not int(CFNumber(userInfo[CFString('SKYPE_API_AVAILABILITY')]))

    def SKSkypeAttachResponse(self, center, observer, name, obj, userInfo):
        self.logger.debug('received SKSkypeAttachResponse')
        # It seems that this notification is not called if the access is refused. Therefore we can't
        # distinguish between attach timeout and access refuse.
        if unicode(CFString(userInfo[CFString('SKYPE_API_CLIENT_NAME')])) == self.friendly_name:
            response = int(CFNumber(userInfo[CFString('SKYPE_API_ATTACH_RESPONSE')]))
            if response and self.client_id == -1:
                self.client_id = response
                self.set_attachment_status(apiAttachSuccess)
