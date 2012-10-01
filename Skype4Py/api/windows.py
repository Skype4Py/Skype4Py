"""
Low level *Skype for Windows* interface implemented using *Windows messaging*.
Uses direct *WinAPI* calls through *ctypes* module.

This module handles the options that you can pass to `Skype.__init__`
for Windows machines.

No options are currently supported.
"""
__docformat__ = 'restructuredtext en'


import sys
import threading
import time
from ctypes import *
import logging

from Skype4Py.api import Command, SkypeAPIBase, \
                         timeout2float, finalize_opts, \
                         DEFAULT_TIMEOUT
from Skype4Py.enums import *
from Skype4Py.errors import SkypeAPIError


__all__ = ['SkypeAPI']


try:
    WNDPROC = WINFUNCTYPE(c_long, c_int, c_uint, c_int, c_int)
except NameError:
    # Proceed only if our setup.py is not running.
    if not getattr(sys, 'skype4py_setup', False):
        raise
    # This will allow importing of this module on non-Windows machines. It won't work
    # of course but this will allow building documentation on any platform.
    WNDPROC = c_void_p


class WNDCLASS(Structure):
    _fields_ = [('style', c_uint),
                ('lpfnWndProc', WNDPROC),
                ('cbClsExtra', c_int),
                ('cbWndExtra', c_int),
                ('hInstance', c_int),
                ('hIcon', c_int),
                ('hCursor', c_int),
                ('hbrBackground', c_int),
                ('lpszMenuName', c_char_p),
                ('lpszClassName', c_char_p)]


class MSG(Structure):
    _fields_ = [('hwnd', c_int),
                ('message', c_uint),
                ('wParam', c_int),
                ('lParam', c_int),
                ('time', c_int),
                ('pointX', c_long),
                ('pointY', c_long)]


class COPYDATASTRUCT(Structure):
    _fields_ = [('dwData', POINTER(c_uint)),
                ('cbData', c_uint),
                ('lpData', c_char_p)]


PCOPYDATASTRUCT = POINTER(COPYDATASTRUCT)

WM_QUIT = 0x12
WM_COPYDATA = 0x4A

HWND_BROADCAST = 0xFFFF


class SkypeAPI(SkypeAPIBase):
    def __init__(self, opts):
        self.logger = logging.getLogger('Skype4Py.api.windows.SkypeAPI')
        SkypeAPIBase.__init__(self)
        finalize_opts(opts)
        self.window_class = None
        self.hwnd = None
        self.skype = None
        self.wait = False
        self.SkypeControlAPIDiscover = windll.user32.RegisterWindowMessageA('SkypeControlAPIDiscover')
        self.SkypeControlAPIAttach = windll.user32.RegisterWindowMessageA('SkypeControlAPIAttach')
        windll.user32.GetWindowLongA.restype = c_ulong

    def run(self):
        self.logger.info('thread started')
        if not self.create_window():
            self.hwnd = None
            return

        msg = MSG()
        pmsg = pointer(msg)
        while self.hwnd and windll.user32.GetMessageA(pmsg, self.hwnd, 0, 0):
            windll.user32.TranslateMessage(pmsg)
            windll.user32.DispatchMessageA(pmsg)

        self.destroy_window()
        self.hwnd = None
        self.logger.info('thread finished')

    def close(self):
        if self.hwnd:
            windll.user32.PostMessageA(self.hwnd, WM_QUIT, 0, 0)
            while self.hwnd:
                time.sleep(0.01)
        self.skype = None
        SkypeAPIBase.close(self)

    def set_friendly_name(self, friendly_name):
        SkypeAPIBase.set_friendly_name(self, friendly_name)
        if self.skype:
            self.send_command(Command('NAME %s' % friendly_name))

    def get_foreground_window(self):
        fhwnd = windll.user32.GetForegroundWindow()
        if fhwnd:
            # awahlig (7.05.2008):
            # I've found at least one app (RocketDock) that had window style 8 set.
            # This is odd since windows header files do not contain such a style.
            # Doing message exchange while this window is a foreground one, causes
            # lockups if some operations on client UI are involved (for example
            # sending a 'FOCUS' command). Therefore, we will set our window as
            # the foreground one for the transmission time.
            if windll.user32.GetWindowLongA(fhwnd, -16) & 8 == 0:
                fhwnd = None
        return fhwnd
        
    def attach(self, timeout, wait=True):
        if self.skype is not None and windll.user32.IsWindow(self.skype):
            return
        self.acquire()
        self.skype = None
        try:
            if not self.isAlive():
                try:
                    self.start()
                except AssertionError:
                    raise SkypeAPIError('Skype API closed')
                # wait till the thread initializes
                while not self.hwnd:
                    time.sleep(0.01)
            self.logger.debug('broadcasting SkypeControlAPIDiscover')
            fhwnd = self.get_foreground_window()
            try:
                if fhwnd:
                    windll.user32.SetForegroundWindow(self.hwnd)
                if not windll.user32.SendMessageTimeoutA(HWND_BROADCAST, self.SkypeControlAPIDiscover,
                                                         self.hwnd, None, 2, 5000, None):
                    raise SkypeAPIError('Could not broadcast Skype discover message')
                # wait (with timeout) till the WindProc() attaches
                self.wait = True
                t = threading.Timer(timeout2float(timeout), lambda: setattr(self, 'wait', False))
                if wait:
                    t.start()
                while self.wait and self.attachment_status not in (apiAttachSuccess, apiAttachRefused):
                    if self.attachment_status == apiAttachPendingAuthorization:
                        # disable the timeout
                        t.cancel()
                    elif self.attachment_status == apiAttachAvailable:
                        # rebroadcast
                        self.logger.debug('broadcasting SkypeControlAPIDiscover')
                        windll.user32.SetForegroundWindow(self.hwnd)
                        if not windll.user32.SendMessageTimeoutA(HWND_BROADCAST, self.SkypeControlAPIDiscover,
                                                                 self.hwnd, None, 2, 5000, None):
                            raise SkypeAPIError('Could not broadcast Skype discover message')
                    time.sleep(0.01)
                t.cancel()
            finally:
                if fhwnd:
                    windll.user32.SetForegroundWindow(fhwnd)
        finally:
            self.release()
        # check if we got the Skype window's hwnd
        if self.skype is not None:
            command = Command('PROTOCOL %s' % self.protocol, Blocking=True)
            self.send_command(command)
            self.protocol = int(command.Reply.rsplit(None, 1)[-1])
        elif not self.wait:
            raise SkypeAPIError('Skype attach timeout')

    def is_running(self):
        # TZap is for Skype 4.0, tSk for 3.8 series
        return bool(windll.user32.FindWindowA('TZapMainForm.UnicodeClass', None) or \
            windll.user32.FindWindowA('tSkMainForm.UnicodeClass', None))

    def get_skype_path(self):
        key = c_long()
        # try to find Skype in HKEY_CURRENT_USER registry tree
        if windll.advapi32.RegOpenKeyA(0x80000001, 'Software\\Skype\\Phone', byref(key)) != 0:
            # try to find Skype in HKEY_LOCAL_MACHINE registry tree
            if windll.advapi32.RegOpenKeyA(0x80000002, 'Software\\Skype\\Phone', byref(key)) != 0:
                raise SkypeAPIError('Skype not installed')
        pathlen = c_long(512)
        path = create_string_buffer(pathlen.value)
        if windll.advapi32.RegQueryValueExA(key, 'SkypePath', None, None, path, byref(pathlen)) != 0:
            windll.advapi32.RegCloseKey(key)
            raise SkypeAPIError('Cannot find Skype path')
        windll.advapi32.RegCloseKey(key)
        return path.value

    def startup(self, minimized, nosplash):
        args = []
        if minimized:
            args.append('/MINIMIZED')
        if nosplash:
            args.append('/NOSPLASH')
        try:
            if self.hwnd:
                fhwnd = self.get_foreground_window()
                if fhwnd:
                    windll.user32.SetForegroundWindow(self.hwnd)
            if windll.shell32.ShellExecuteA(None, 'open', self.get_skype_path(), ' '.join(args), None, 0) <= 32:
                raise SkypeAPIError('Could not start Skype')
        finally:
            if self.hwnd and fhwnd:
                windll.user32.SetForegroundWindow(fhwnd)
        
    def shutdown(self):
        try:
            if self.hwnd:
                fhwnd = self.get_foreground_window()
                if fhwnd:
                    windll.user32.SetForegroundWindow(self.hwnd)
            if windll.shell32.ShellExecuteA(None, 'open', self.get_skype_path(), '/SHUTDOWN', None, 0) <= 32:
                raise SkypeAPIError('Could not shutdown Skype')
        finally:
            if self.hwnd and fhwnd:
                windll.user32.SetForegroundWindow(fhwnd)

    def create_window(self):
        # window class has to be saved as property to keep reference to self.WinProc
        self.window_class = WNDCLASS(3, WNDPROC(self.window_proc), 0, 0,
                                     windll.kernel32.GetModuleHandleA(None),
                                     0, 0, 0, None, 'Skype4Py.%d' % id(self))

        wclass = windll.user32.RegisterClassA(byref(self.window_class))
        if wclass == 0:
            return False

        self.hwnd = windll.user32.CreateWindowExA(0, 'Skype4Py.%d' % id(self), 'Skype4Py',
                                                  0xCF0000, 0x80000000, 0x80000000,
                                                  0x80000000, 0x80000000, None, None,
                                                  self.window_class.hInstance, 0)
        if self.hwnd == 0:
            windll.user32.UnregisterClassA('Skype4Py.%d' % id(self), None)
            return False

        return True

    def destroy_window(self):
        if not windll.user32.DestroyWindow(self.hwnd):
            return False
        self.hwnd = None

        if not windll.user32.UnregisterClassA('Skype4Py.%d' % id(self), None):
            return False
        self.window_class = None

        return True

    def window_proc(self, hwnd, umsg, wparam, lparam):
        if umsg == self.SkypeControlAPIAttach:
            self.logger.debug('received SkypeControlAPIAttach %s', lparam)
            if lparam == apiAttachSuccess:
                if self.skype is None or self.skype == wparam:
                    self.skype = wparam
                else:
                    self.logger.warning('second successful attach received for different API window')
            elif lparam in (apiAttachRefused, apiAttachNotAvailable, apiAttachAvailable):
                self.skype = None
            elif lparam == apiAttachPendingAuthorization:
                if self.attachment_status == apiAttachSuccess:
                    self.logger.warning('received pending attach after successful attach')
                    return 0
            self.set_attachment_status(lparam)
            return 1
        elif umsg == WM_COPYDATA and wparam == self.skype and lparam:
            copydata = cast(lparam, PCOPYDATASTRUCT).contents
            cmd8 = copydata.lpData[:copydata.cbData - 1]
            cmd = cmd8.decode('utf-8')
            self.logger.debug('received %s', repr(cmd))
            if cmd.startswith(u'#'):
                p = cmd.find(u' ')
                command = self.pop_command(int(cmd[1:p]))
                if command is not None:
                    command.Reply = cmd[p + 1:]
                    if command.Blocking:
                        command._event.set()
                    else:
                        command._timer.cancel()
                    self.notifier.reply_received(command)
                else:
                    self.notifier.notification_received(cmd[p + 1:])
            else:
                self.notifier.notification_received(cmd)
            return 1
        elif umsg == apiAttachAvailable:
            self.logger.debug('received apiAttachAvailable')
            self.skype = None
            self.set_attachment_status(umsg)
            return 1
        return windll.user32.DefWindowProcA(c_int(hwnd), c_int(umsg), c_int(wparam), c_int(lparam))

    def send_command(self, command):
        for retry in xrange(2):
            if self.skype is None:
                self.attach(command.Timeout)
            self.push_command(command)
            self.notifier.sending_command(command)
            cmd = u'#%d %s' % (command.Id, command.Command)
            cmd8 = cmd.encode('utf-8') + '\0'
            copydata = COPYDATASTRUCT(None, len(cmd8), cmd8)
            if command.Blocking:
                command._event = event = threading.Event()
            else:
                command._timer = timer = threading.Timer(command.timeout2float(), self.pop_command, (command.Id,))
            self.logger.debug('sending %s', repr(cmd))
            fhwnd = self.get_foreground_window()
            try:
                if fhwnd:
                    windll.user32.SetForegroundWindow(self.hwnd)
                if windll.user32.SendMessageA(self.skype, WM_COPYDATA, self.hwnd, byref(copydata)):
                    if command.Blocking:
                        event.wait(command.timeout2float())
                        if not event.isSet():
                            raise SkypeAPIError('Skype command timeout')
                    else:
                        timer.start()
                    break
                else:
                    # SendMessage failed
                    self.pop_command(command.Id)
                    self.skype = None
                    # let the loop go back and try to reattach but only once
            finally:
                if fhwnd:
                    windll.user32.SetForegroundWindow(fhwnd)
        else:
            raise SkypeAPIError('Skype API error, check if Skype wasn\'t closed')

    def allow_focus(self, timeout):
        if self.skype is None:
            self.attach(timeout)
        process_id = c_ulong()
        windll.user32.GetWindowThreadProcessId(self.skype, byref(process_id))
        if process_id:
            windll.user32.AllowSetForegroundWindow(process_id)
