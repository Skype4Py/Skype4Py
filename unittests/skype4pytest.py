import sys
import os
import unittest
import logging
import threading

# Add the parent directory to the top of the search paths list so the
# distribution copy of the Skype4Py module can be imported instead of
# the installed one.
sys.path.insert(0, os.path.abspath('..'))

import Skype4Py
from Skype4Py.skype import *
from Skype4Py.api import SkypeAPIBase


class SkypeAPI(SkypeAPIBase):
    def __init__(self):
        SkypeAPIBase.__init__(self)
        self.queue = []
        
    def attach(self, timeout, wait=True):
        self.set_attachment_status(apiAttachSuccess)
        
    def send_command(self, command):
        self.push_command(command)
        try:
            self.notifier.sending_command(command)
            try:
                cmd, reply = self.dequeue()
            except IndexError:
                raise SkypeAPIError('expected [%s] command in the queue' % command.Command)
            if cmd != command.Command:
                raise SkypeAPIError('expected [%s] command in the queue, not [%s]' %
                                    (command.Command, cmd))
            command.Reply = reply
            self.notifier.reply_received(command)
            if cmd[:4].upper() == 'SET ':
                self.schedule(0.1, reply)
        finally:
            self.pop_command(command.Id)

    def enqueue(self, cmd, reply=None):
        assert cmd
        if reply is None:
            reply = cmd
        self.queue.append((unicode(cmd), unicode(reply)))
        
    def dequeue(self):
        return self.queue.pop(0)
        
    def is_empty(self):
        return not self.queue

    def clear(self):
        del self.queue[:]

    def schedule(self, timeout, cmd):
        timer = threading.Timer(timeout, self.notifier.notification_received, [cmd])
        timer.start()


class TestCase(unittest.TestCase):
    '''The base for all Skype4Py test cases. Creates an instance
    of Skype4Py.Skype and attaches it to the running Skype client.
    '''
    
    def setUp(self):
        self.api = SkypeAPI()
        self.skype = Skype4Py.Skype(Api=self.api)
        self.skype.FriendlyName = 'Skype4Py-%s' % self.__class__.__name__
        self.skype.Attach()
        self.setUpObject()
        
    def tearDown(self):
        self.tearDownObject()
        del self.skype
        del self.api

    def setUpObject(self):
        '''Override to set the "obj" attribute to the tested Skype4Py object.
        '''
        self.obj = None
        
    def tearDownObject(self):
        '''Override to delete the tested object ("obj" attribute).
        '''
        del self.obj
                
    def assertInstance(self, value, types):
        '''Tests if value is an instance of types which may be a type or
        tuple of types (in which case value type may be one them).
        '''
        self.failUnless(isinstance(value, types),
            '%s is not an instance of %s' % (repr(value), types))

    def skypeVersionInfo(self):
        return tuple(map(int, self.skype.Version.split('.')))


def suite():
    import applicationtest
    import calltest
    import chattest
    import clienttest
    import filetransfertest
    import profiletest
    import settingstest
    import skypetest
    import smstest
    import usertest
    import voicemailtest

    return unittest.TestSuite([
        applicationtest.suite(),
        calltest.suite(),
        chattest.suite(),
        clienttest.suite(),
        filetransfertest.suite(),
        profiletest.suite(),
        settingstest.suite(),
        skypetest.suite(),
        smstest.suite(),
        usertest.suite(),
        voicemailtest.suite(),
    ])


if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser(usage='Usage: %prog [options] [test] [...]')
    parser.add_option('-v', '--verbose',
                      action='store_const', const=2, dest='verbosity',
                      help='verbose output')
    parser.add_option('-q', '--quiet',
                      action='store_const', const=0, dest='verbosity',
                      help='minimal output')
    parser.add_option('-d', '--debug', action='store_true',
                      help='enable Skype4Py debugging')

    options, args = parser.parse_args()

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)

    if args:
        suite = unittest.defaultTestLoader.loadTestsFromNames(args)
    else:
        suite = suite()

    unittest.TextTestRunner(verbosity=options.verbosity).run(suite)
