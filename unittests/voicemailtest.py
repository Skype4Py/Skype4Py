import unittest

import skype4pytest
from Skype4Py.voicemail import *


class VoicemailTest(skype4pytest.TestCase):
    def setUpObject(self):
        self.obj = Voicemail(self.skype, '1234')

    # Methods
    # =======

    def testCaptureMicDevice(self):
        # Returned type: unicode, dict or None
        self.api.enqueue('GET VOICEMAIL 1234 CAPTURE_MIC',
                         'VOICEMAIL 1234 CAPTURE_MIC file="c:\\spam.wav"')
        t = self.obj.CaptureMicDevice()
        self.assertInstance(t, dict)
        self.assertEqual(t, {u'file': 'c:\\spam.wav'})
        self.failUnless(self.api.is_empty())

    def testDelete(self):
        self.api.enqueue('ALTER VOICEMAIL 1234 DELETE')
        self.obj.Delete()
        self.failUnless(self.api.is_empty())

    def testDownload(self):
        self.api.enqueue('ALTER VOICEMAIL 1234 DOWNLOAD')
        self.obj.Download()
        self.failUnless(self.api.is_empty())

    def testInputDevice(self):
        # Returned type: unicode, dict or None
        self.api.enqueue('GET VOICEMAIL 1234 INPUT',
                         'VOICEMAIL 1234 INPUT file="c:\\spam.wav"')
        t = self.obj.InputDevice('file')
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'c:\\spam.wav')
        self.failUnless(self.api.is_empty())

    def testOpen(self):
        self.api.enqueue('OPEN VOICEMAIL 1234')
        self.obj.Open()
        self.failUnless(self.api.is_empty())

    def testOutputDevice(self):
        # Returned type: unicode, dict or None
        self.api.enqueue('GET VOICEMAIL 1234 OUTPUT',
                         'VOICEMAIL 1234 OUTPUT')
        self.api.enqueue('ALTER VOICEMAIL 1234 SET_OUTPUT file="c:\\spam.wav"')
        self.obj.OutputDevice('file', 'c:\\spam.wav')
        self.failUnless(self.api.is_empty())

    def testSetUnplayed(self):
        self.api.enqueue('ALTER VOICEMAIL 1234 SETUNPLAYED')
        self.obj.SetUnplayed()
        self.failUnless(self.api.is_empty())

    def testStartPlayback(self):
        self.api.enqueue('ALTER VOICEMAIL 1234 STARTPLAYBACK')
        self.obj.StartPlayback()
        self.failUnless(self.api.is_empty())

    def testStartPlaybackInCall(self):
        self.api.enqueue('ALTER VOICEMAIL 1234 STARTPLAYBACKINCALL')
        self.obj.StartPlaybackInCall()
        self.failUnless(self.api.is_empty())

    def testStartRecording(self):
        self.api.enqueue('ALTER VOICEMAIL 1234 STARTRECORDING')
        self.obj.StartRecording()
        self.failUnless(self.api.is_empty())

    def testStopPlayback(self):
        self.api.enqueue('ALTER VOICEMAIL 1234 STOPPLAYBACK')
        self.obj.StopPlayback()
        self.failUnless(self.api.is_empty())

    def testStopRecording(self):
        self.api.enqueue('ALTER VOICEMAIL 1234 STOPRECORDING')
        self.obj.StopRecording()
        self.failUnless(self.api.is_empty())

    def testUpload(self):
        self.api.enqueue('ALTER VOICEMAIL 1234 UPLOAD')
        self.obj.Upload()
        self.failUnless(self.api.is_empty())

    # Properties
    # ==========

    def testAllowedDuration(self):
        # Readable, Type: int
        self.api.enqueue('GET VOICEMAIL 1234 ALLOWED_DURATION',
                         'VOICEMAIL 1234 ALLOWED_DURATION 123')
        t = self.obj.AllowedDuration
        self.assertInstance(t, int)
        self.assertEqual(t, 123)
        self.failUnless(self.api.is_empty())

    def testDatetime(self):
        # Readable, Type: datetime
        from datetime import datetime
        from time import time
        now = time()
        self.api.enqueue('GET VOICEMAIL 1234 TIMESTAMP',
                         'VOICEMAIL 1234 TIMESTAMP %f' % now)
        t = self.obj.Datetime
        self.assertInstance(t, datetime)
        self.assertEqual(t, datetime.fromtimestamp(now))
        self.failUnless(self.api.is_empty())

    def testDuration(self):
        # Readable, Type: int
        self.api.enqueue('GET VOICEMAIL 1234 DURATION',
                         'VOICEMAIL 1234 DURATION 123')
        t = self.obj.Duration
        self.assertInstance(t, int)
        self.assertEqual(t, 123)
        self.failUnless(self.api.is_empty())

    def testFailureReason(self):
        # Readable, Type: str
        self.api.enqueue('GET VOICEMAIL 1234 FAILUREREASON',
                         'VOICEMAIL 1234 FAILUREREASON eggs')
        t = self.obj.FailureReason
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testId(self):
        # Readable, Type: int
        t = self.obj.Id
        self.assertInstance(t, int)
        self.assertEqual(t, 1234)

    def testPartnerDisplayName(self):
        # Readable, Type: unicode
        self.api.enqueue('GET VOICEMAIL 1234 PARTNER_DISPNAME',
                         'VOICEMAIL 1234 PARTNER_DISPNAME eggs')
        t = self.obj.PartnerDisplayName
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testPartnerHandle(self):
        # Readable, Type: str
        self.api.enqueue('GET VOICEMAIL 1234 PARTNER_HANDLE',
                         'VOICEMAIL 1234 PARTNER_HANDLE eggs')
        t = self.obj.PartnerHandle
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testStatus(self):
        # Readable, Type: str
        self.api.enqueue('GET VOICEMAIL 1234 STATUS',
                         'VOICEMAIL 1234 STATUS DOWNLOADING')
        t = self.obj.Status
        self.assertInstance(t, str)
        self.assertEqual(t, 'DOWNLOADING')
        self.failUnless(self.api.is_empty())

    def testTimestamp(self):
        # Readable, Type: float
        self.api.enqueue('GET VOICEMAIL 1234 TIMESTAMP',
                         'VOICEMAIL 1234 TIMESTAMP 123.4')
        t = self.obj.Timestamp
        self.assertInstance(t, float)
        self.assertEqual(t, 123.4)
        self.failUnless(self.api.is_empty())

    def testType(self):
        # Readable, Type: str
        self.api.enqueue('GET VOICEMAIL 1234 TYPE',
                         'VOICEMAIL 1234 TYPE OUTGOING')
        t = self.obj.Type
        self.assertInstance(t, str)
        self.assertEqual(t, 'OUTGOING')
        self.failUnless(self.api.is_empty())


def suite():
    return unittest.TestSuite([
        unittest.defaultTestLoader.loadTestsFromTestCase(VoicemailTest),
    ])


if __name__ == '__main__':
    unittest.main()
