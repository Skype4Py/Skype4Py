import unittest

import skype4pytest
from Skype4Py.settings import *


class SettingsTest(skype4pytest.TestCase):
    def setUpObject(self):
        self.obj = self.skype.Settings

    # Methods
    # =======

    def testAvatar(self):
        from warnings import simplefilter
        self.api.enqueue('SET AVATAR 1 c:\\spam.jpg',
                         'AVATAR 1 c:\\spam.jpg')
        simplefilter('ignore')
        try:
            self.obj.Avatar(1, 'c:\\spam.jpg')
        finally:
            simplefilter('default')
        self.failUnless(self.api.is_empty())

    def testLoadAvatarFromFile(self):
        self.api.enqueue('SET AVATAR 1 c:\\spam.jpg',
                         'AVATAR 1 c:\\spam.jpg')
        self.obj.LoadAvatarFromFile('c:\\spam.jpg')
        self.failUnless(self.api.is_empty())

    def testResetIdleTimer(self):
        self.api.enqueue('RESETIDLETIMER')
        self.obj.ResetIdleTimer()
        self.failUnless(self.api.is_empty())

    def testRingTone(self):
        # Returned type: str or None
        self.api.enqueue('GET RINGTONE 1',
                         'RINGTONE 1 c:\\spam.wav')
        t = self.obj.RingTone()
        self.assertInstance(t, str)
        self.assertEqual(t, 'c:\\spam.wav')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET RINGTONE 1 c:\\spam.wav',
                         'RINGTONE 1 c:\\spam.wav')
        self.obj.RingTone(1, 'c:\\spam.wav')
        self.failUnless(self.api.is_empty())

    def testRingToneStatus(self):
        # Returned type: bool
        self.api.enqueue('GET RINGTONE 1 STATUS',
                         'RINGTONE 1 STATUS ON')
        t = self.obj.RingToneStatus(1)
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET RINGTONE 1 STATUS OFF',
                         'RINGTONE 1 STATUS OFF')
        self.obj.RingToneStatus(1, False)
        self.failUnless(self.api.is_empty())

    def testSaveAvatarToFile(self):
        self.api.enqueue('GET AVATAR 1 c:\\spam.jpg',
                         'AVATAR 1 c:\\spam.jpg')
        self.obj.SaveAvatarToFile('c:\\spam.jpg')
        self.failUnless(self.api.is_empty())

    # Properties
    # ==========

    def testAEC(self):
        # Readable, Writable, Type: bool
        self.api.enqueue('GET AEC',
                         'AEC ON')
        t = self.obj.AEC
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET AEC OFF',
                         'AEC OFF')
        self.obj.AEC = False
        self.failUnless(self.api.is_empty())

    def testAGC(self):
        # Readable, Writable, Type: bool
        self.api.enqueue('GET AGC',
                         'AGC ON')
        t = self.obj.AGC
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET AGC OFF',
                         'AGC OFF')
        self.obj.AGC = False
        self.failUnless(self.api.is_empty())

    def testAudioIn(self):
        # Readable, Writable, Type: unicode
        self.api.enqueue('GET AUDIO_IN',
                         'AUDIO_IN eggs')
        t = self.obj.AudioIn
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET AUDIO_IN eggs',
                         'AUDIO_IN eggs')
        self.obj.AudioIn = 'eggs'
        self.failUnless(self.api.is_empty())

    def testAudioOut(self):
        # Readable, Writable, Type: unicode
        self.api.enqueue('GET AUDIO_OUT',
                         'AUDIO_OUT eggs')
        t = self.obj.AudioOut
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET AUDIO_OUT eggs',
                         'AUDIO_OUT eggs')
        self.obj.AudioOut = 'eggs'
        self.failUnless(self.api.is_empty())

    def testAutoAway(self):
        # Readable, Writable, Type: bool
        self.api.enqueue('GET AUTOAWAY',
                         'AUTOAWAY ON')
        t = self.obj.AutoAway
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET AUTOAWAY OFF',
                         'AUTOAWAY OFF')
        self.obj.AutoAway = False
        self.failUnless(self.api.is_empty())

    def testLanguage(self):
        # Readable, Writable, Type: str
        self.api.enqueue('GET UI_LANGUAGE',
                         'UI_LANGUAGE de')
        t = self.obj.Language
        self.assertInstance(t, str)
        self.assertEqual(t, 'de')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET UI_LANGUAGE de',
                         'UI_LANGUAGE de')
        self.obj.Language = 'de'
        self.failUnless(self.api.is_empty())

    def testPCSpeaker(self):
        # Readable, Writable, Type: bool
        self.api.enqueue('GET PCSPEAKER',
                         'PCSPEAKER ON')
        t = self.obj.PCSpeaker
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET PCSPEAKER OFF',
                         'PCSPEAKER OFF')
        self.obj.PCSpeaker = False
        self.failUnless(self.api.is_empty())

    def testRinger(self):
        # Readable, Writable, Type: unicode
        self.api.enqueue('GET RINGER',
                         'RINGER eggs')
        t = self.obj.Ringer
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET RINGER eggs',
                         'RINGER eggs')
        self.obj.Ringer = 'eggs'
        self.failUnless(self.api.is_empty())

    def testVideoIn(self):
        # Readable, Writable, Type: unicode
        self.api.enqueue('GET VIDEO_IN',
                         'VIDEO_IN eggs')
        t = self.obj.VideoIn
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET VIDEO_IN ',
                         'VIDEO_IN')
        self.obj.VideoIn = ''
        self.failUnless(self.api.is_empty())


def suite():
    return unittest.TestSuite([
        unittest.defaultTestLoader.loadTestsFromTestCase(SettingsTest),
    ])


if __name__ == '__main__':
    unittest.main()
