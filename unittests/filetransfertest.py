import unittest

import skype4pytest
from Skype4Py.filetransfer import *


class FileTransferTest(skype4pytest.TestCase):
    def setUpObject(self):
        self.obj = FileTransfer(self.skype, '1234')

    # Properties
    # ==========

    def testBytesPerSecond(self):
        # Readable, Type: int
        self.api.enqueue('GET FILETRANSFER 1234 BYTESPERSECOND',
                         'FILETRANSFER 1234 BYTESPERSECOND 123')
        t = self.obj.BytesPerSecond
        self.assertInstance(t, int)
        self.assertEqual(t, 123)
        self.failUnless(self.api.is_empty())

    def testBytesTransferred(self):
        # Readable, Type: long
        self.api.enqueue('GET FILETRANSFER 1234 BYTESTRANSFERRED',
                         'FILETRANSFER 1234 BYTESTRANSFERRED 12345')
        t = self.obj.BytesTransferred
        self.assertInstance(t, long)
        self.assertEqual(t, 12345)
        self.failUnless(self.api.is_empty())

    def testFailureReason(self):
        # Readable, Type: str
        self.api.enqueue('GET FILETRANSFER 1234 FAILUREREASON',
                         'FILETRANSFER 1234 FAILUREREASON FAILED_READ')
        t = self.obj.FailureReason
        self.assertInstance(t, str)
        self.assertEqual(t, 'FAILED_READ')
        self.failUnless(self.api.is_empty())

    def testFileName(self):
        # Readable, Type: str
        self.api.enqueue('GET FILETRANSFER 1234 FILEPATH',
                         'FILETRANSFER 1234 FILEPATH \\spam\\eggs')
        t = self.obj.FileName
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testFilePath(self):
        # Readable, Type: str
        self.api.enqueue('GET FILETRANSFER 1234 FILEPATH',
                         'FILETRANSFER 1234 FILEPATH \\spam\\eggs')
        t = self.obj.FilePath
        self.assertInstance(t, str)
        self.assertEqual(t, '\\spam\\eggs')
        self.failUnless(self.api.is_empty())

    def testFileSize(self):
        # Readable, Type: long
        self.api.enqueue('GET FILETRANSFER 1234 FILESIZE',
                         'FILETRANSFER 1234 FILESIZE 12345')
        t = self.obj.FileSize
        self.assertInstance(t, long)
        self.assertEqual(t, 12345)
        self.failUnless(self.api.is_empty())

    def testFinishDatetime(self):
        # Readable, Type: datetime
        from datetime import datetime
        from time import time
        now = time()
        self.api.enqueue('GET FILETRANSFER 1234 FINISHTIME',
                         'FILETRANSFER 1234 FINISHTIME %f' % now)
        t = self.obj.FinishDatetime
        self.assertInstance(t, datetime)
        self.assertEqual(t, datetime.fromtimestamp(now))
        self.failUnless(self.api.is_empty())

    def testFinishTime(self):
        # Readable, Type: float
        self.api.enqueue('GET FILETRANSFER 1234 FINISHTIME',
                         'FILETRANSFER 1234 FINISHTIME 123.4')
        t = self.obj.FinishTime
        self.assertInstance(t, float)
        self.assertEqual(t, 123.4)
        self.failUnless(self.api.is_empty())

    def testId(self):
        # Readable, Type: int
        t = self.obj.Id
        self.assertInstance(t, int)
        self.assertEqual(t, 1234)

    def testPartnerDisplayName(self):
        # Readable, Type: unicode
        self.api.enqueue('GET FILETRANSFER 1234 PARTNER_DISPNAME',
                         'FILETRANSFER 1234 PARTNER_DISPNAME eggs')
        t = self.obj.PartnerDisplayName
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testPartnerHandle(self):
        # Readable, Type: str
        self.api.enqueue('GET FILETRANSFER 1234 PARTNER_HANDLE',
                         'FILETRANSFER 1234 PARTNER_HANDLE eggs')
        t = self.obj.PartnerHandle
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testStartDatetime(self):
        # Readable, Type: datetime
        from datetime import datetime
        from time import time
        now = time()
        self.api.enqueue('GET FILETRANSFER 1234 STARTTIME',
                         'FILETRANSFER 1234 STARTTIME %f' % now)
        t = self.obj.StartDatetime
        self.assertInstance(t, datetime)
        self.assertEqual(t, datetime.fromtimestamp(now))
        self.failUnless(self.api.is_empty())

    def testStartTime(self):
        # Readable, Type: float
        self.api.enqueue('GET FILETRANSFER 1234 STARTTIME',
                         'FILETRANSFER 1234 STARTTIME 123.4')
        t = self.obj.StartTime
        self.assertInstance(t, float)
        self.assertEqual(t, 123.4)
        self.failUnless(self.api.is_empty())

    def testStatus(self):
        # Readable, Type: str
        self.api.enqueue('GET FILETRANSFER 1234 STATUS',
                         'FILETRANSFER 1234 STATUS PAUSED')
        t = self.obj.Status
        self.assertInstance(t, str)
        self.assertEqual(t, 'PAUSED')
        self.failUnless(self.api.is_empty())

    def testType(self):
        # Readable, Type: str
        self.api.enqueue('GET FILETRANSFER 1234 TYPE',
                         'FILETRANSFER 1234 TYPE INCOMING')
        t = self.obj.Type
        self.assertInstance(t, str)
        self.assertEqual(t, 'INCOMING')
        self.failUnless(self.api.is_empty())


def suite():
    return unittest.TestSuite([
        unittest.defaultTestLoader.loadTestsFromTestCase(FileTransferTest),
    ])


if __name__ == '__main__':
    unittest.main()
