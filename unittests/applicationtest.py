import unittest

import skype4pytest
from Skype4Py.application import *


class ApplicationTest(skype4pytest.TestCase):
    def setUpObject(self):
        self.obj = Application(self.skype, 'spam')

    # Methods
    # =======

    def testConnect(self):
        # Returned type: ApplicationStream or None
        self.api.enqueue('GET APPLICATION spam STREAMS',
                         'APPLICATION spam STREAMS')
        self.api.enqueue('ALTER APPLICATION spam CONNECT eggs')
        self.api.schedule(0.1, 'APPLICATION spam STREAMS eggs:1')
        t = self.obj.Connect('eggs', WaitConnected=True)
        self.assertInstance(t, ApplicationStream)
        self.assertEqual(t.Handle, 'eggs:1')
        self.failUnless(self.api.is_empty())

    def testCreate(self):
        self.api.enqueue('CREATE APPLICATION spam')
        self.obj.Create()
        self.failUnless(self.api.is_empty())

    def testDelete(self):
        self.api.enqueue('DELETE APPLICATION spam')
        self.obj.Delete()
        self.failUnless(self.api.is_empty())

    def testSendDatagram(self):
        self.api.enqueue('GET APPLICATION spam STREAMS',
                         'APPLICATION spam STREAMS eggs:1')
        self.api.enqueue('ALTER APPLICATION spam DATAGRAM eggs:1 sausage')
        self.obj.SendDatagram('sausage')
        self.failUnless(self.api.is_empty())

    # Properties
    # ==========

    def testConnectableUsers(self):
        # Readable, Type: UserCollection
        self.api.enqueue('GET APPLICATION spam CONNECTABLE',
                         'APPLICATION spam CONNECTABLE eggs, ham')
        t = self.obj.ConnectableUsers
        self.assertInstance(t, UserCollection)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())

    def testConnectingUsers(self):
        # Readable, Type: UserCollection
        self.api.enqueue('GET APPLICATION spam CONNECTING',
                         'APPLICATION spam CONNECTING eggs, ham, sausage')
        t = self.obj.ConnectingUsers
        self.assertInstance(t, UserCollection)
        self.assertEqual(len(t), 3)
        self.failUnless(self.api.is_empty())

    def testName(self):
        # Readable, Type: unicode
        t = self.obj.Name
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'spam')

    def testReceivedStreams(self):
        # Readable, Type: ApplicationStreamCollection
        self.api.enqueue('GET APPLICATION spam RECEIVED',
                         'APPLICATION spam RECEIVED sausage:1 eggs:3')
        t = self.obj.ReceivedStreams
        self.assertInstance(t, ApplicationStreamCollection)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())

    def _testSendingStreams(self):
        # Readable, Type: ApplicationStreamCollection
        self.api.enqueue('GET APPLICATION spam SENDING',
                         'APPLICATION spam SENDING eggs:2 ham:5 bacon:7')
        t = self.obj.SendingStreams
        self.assertInstance(t, ApplicationStreamCollection)
        self.assertEqual(len(t), 7)
        self.failUnless(self.api.is_empty())

    def testStreams(self):
        # Readable, Type: ApplicationStreamCollection
        self.api.enqueue('GET APPLICATION spam STREAMS',
                         'APPLICATION spam STREAMS bacon:1')
        t = self.obj.Streams
        self.assertInstance(t, ApplicationStreamCollection)
        self.assertEqual(len(t), 1)
        self.failUnless(self.api.is_empty())


class ApplicationStreamTest(skype4pytest.TestCase):
    def setUpObject(self):
        app = Application(self.skype, 'spam')
        self.obj = ApplicationStream(app, 'eggs:1')

    # Methods
    # =======

    def testDisconnect(self):
        self.api.enqueue('ALTER APPLICATION spam DISCONNECT eggs:1')
        self.obj.Disconnect()
        self.failUnless(self.api.is_empty())

    def testRead(self):
        # Returned type: unicode
        self.api.enqueue('ALTER APPLICATION spam READ eggs:1',
                         'ALTER APPLICATION spam READ eggs:1 ham')
        t = self.obj.Read()
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'ham')
        self.failUnless(self.api.is_empty())

    def testSendDatagram(self):
        self.api.enqueue('ALTER APPLICATION spam DATAGRAM eggs:1 ham',
                         'ALTER APPLICATION spam DATAGRAM eggs:1')
        self.obj.SendDatagram('ham')
        self.failUnless(self.api.is_empty())

    def testWrite(self):
        self.api.enqueue('ALTER APPLICATION spam WRITE eggs:1 ham',
                         'ALTER APPLICATION spam WRITE eggs:1')
        self.obj.Write('ham')
        self.failUnless(self.api.is_empty())

    # Properties
    # ==========

    def testApplication(self):
        # Readable, Type: Application
        t = self.obj.Application
        self.assertInstance(t, Application)
        self.assertEqual(t.Name, 'spam')

    def testApplicationName(self):
        # Readable, Type: unicode
        t = self.obj.ApplicationName
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'spam')

    def testDataLength(self):
        # Readable, Type: int
        self.api.enqueue('GET APPLICATION spam SENDING',
                         'APPLICATION spam SENDING')
        self.api.enqueue('GET APPLICATION spam RECEIVED',
                         'APPLICATION spam RECEIVED eggs:1=123')
        t = self.obj.DataLength
        self.assertInstance(t, int)
        self.assertEqual(t, 123)
        self.failUnless(self.api.is_empty())

    def testHandle(self):
        # Readable, Type: str
        t = self.obj.Handle
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs:1')

    def testPartnerHandle(self):
        # Readable, Type: str
        t = self.obj.PartnerHandle
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')


def suite():
    return unittest.TestSuite([
        unittest.defaultTestLoader.loadTestsFromTestCase(ApplicationTest),
        unittest.defaultTestLoader.loadTestsFromTestCase(ApplicationStreamTest),
    ])


if __name__ == '__main__':
    unittest.main()
