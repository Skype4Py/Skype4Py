import unittest

import skype4pytest
from Skype4Py.call import *


class CallTest(skype4pytest.TestCase):
    def setUpObject(self):
        self.obj = Call(self.skype, '1234')

    # Methods
    # =======

    def testAnswer(self):
        self.api.enqueue('ALTER CALL 1234 ANSWER')
        self.obj.Answer()
        self.failUnless(self.api.is_empty())

    def testCanTransfer(self):
        # Returned type: bool
        self.api.enqueue('GET CALL 1234 CAN_TRANSFER +3721234567',
                         'CALL 1234 CAN_TRANSFER +3721234567 TRUE')
        t = self.obj.CanTransfer('+3721234567')
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())

    def testCaptureMicDevice(self):
        # Returned type: unicode, dict or None
        self.api.enqueue('GET CALL 1234 CAPTURE_MIC',
                         'CALL 1234 CAPTURE_MIC file="c:\\spam.wav"')
        t = self.obj.CaptureMicDevice()
        self.assertInstance(t, dict)
        self.assertEqual(t, {u'file': 'c:\\spam.wav'})
        self.failUnless(self.api.is_empty())

    def testFinish(self):
        self.api.enqueue('ALTER CALL 1234 END HANGUP')
        self.obj.Finish()
        self.failUnless(self.api.is_empty())

    def testForward(self):
        self.api.enqueue('ALTER CALL 1234 END FORWARD_CALL')
        self.obj.Forward()
        self.failUnless(self.api.is_empty())

    def testHold(self):
        self.api.enqueue('ALTER CALL 1234 HOLD')
        self.obj.Hold()
        self.failUnless(self.api.is_empty())

    def testInputDevice(self):
        # Returned type: unicode, dict or None
        self.api.enqueue('GET CALL 1234 INPUT',
                         'CALL 1234 INPUT file="c:\\spam.wav"')
        t = self.obj.InputDevice('file')
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'c:\\spam.wav')
        self.failUnless(self.api.is_empty())

    def testJoin(self):
        # Returned type: Conference
        self.api.enqueue('SET CALL 1234 JOIN_CONFERENCE 5678',
                         'CALL 1234 CONF_ID 90')
        t = self.obj.Join(5678)
        self.assertInstance(t, Conference)
        self.assertEqual(t.Id, 90)
        self.failUnless(self.api.is_empty())

    def testMarkAsSeen(self):
        self.api.enqueue('SET CALL 1234 SEEN TRUE',
                         'CALL 1234 SEEN TRUE')
        self.obj.MarkAsSeen()
        self.failUnless(self.api.is_empty())

    def testOutputDevice(self):
        # Returned type: unicode, dict or None
        self.api.enqueue('GET CALL 1234 OUTPUT',
                         'CALL 1234 OUTPUT')
        self.api.enqueue('ALTER CALL 1234 SET_OUTPUT file="c:\\spam.wav"')
        self.obj.OutputDevice('file', 'c:\\spam.wav')
        self.failUnless(self.api.is_empty())

    def testRedirectToVoicemail(self):
        self.api.enqueue('ALTER CALL 1234 END REDIRECT_TO_VOICEMAIL')
        self.obj.RedirectToVoicemail()
        self.failUnless(self.api.is_empty())

    def testResume(self):
        self.api.enqueue('ALTER CALL 1234 RESUME')
        self.obj.Resume()
        self.failUnless(self.api.is_empty())

    def testStartVideoReceive(self):
        self.api.enqueue('ALTER CALL 1234 START_VIDEO_RECEIVE')
        self.obj.StartVideoReceive()
        self.failUnless(self.api.is_empty())

    def testStartVideoSend(self):
        self.api.enqueue('ALTER CALL 1234 START_VIDEO_SEND')
        self.obj.StartVideoSend()
        self.failUnless(self.api.is_empty())

    def testStopVideoReceive(self):
        self.api.enqueue('ALTER CALL 1234 STOP_VIDEO_RECEIVE')
        self.obj.StopVideoReceive()
        self.failUnless(self.api.is_empty())

    def testStopVideoSend(self):
        self.api.enqueue('ALTER CALL 1234 STOP_VIDEO_SEND')
        self.obj.StopVideoSend()
        self.failUnless(self.api.is_empty())

    def testTransfer(self):
        self.api.enqueue('ALTER CALL 1234 TRANSFER spam')
        self.obj.Transfer('spam')
        self.failUnless(self.api.is_empty())

    # Properties
    # ==========

    def testConferenceId(self):
        # Readable, Type: int
        self.api.enqueue('GET CALL 1234 CONF_ID',
                         'CALL 1234 CONF_ID 123')
        t = self.obj.ConferenceId
        self.assertInstance(t, int)
        self.assertEqual(t, 123)
        self.failUnless(self.api.is_empty())

    def testDatetime(self):
        # Readable, Type: datetime
        from time import time
        from datetime import datetime
        now = time()
        self.api.enqueue('GET CALL 1234 TIMESTAMP',
                         'CALL 1234 TIMESTAMP %f' % now)
        t = self.obj.Datetime
        self.assertInstance(t, datetime)
        self.assertEqual(t, datetime.fromtimestamp(now))
        self.failUnless(self.api.is_empty())

    def testDTMF(self):
        # Writable, Type: str
        self.api.enqueue('ALTER CALL 1234 DTMF 567890')
        self.obj.DTMF = '567890'
        self.failUnless(self.api.is_empty())

    def testDuration(self):
        # Readable, Type: int
        self.api.enqueue('GET CALL 1234 DURATION',
                         'CALL 1234 DURATION 567')
        t = self.obj.Duration
        self.assertInstance(t, int)
        self.assertEqual(t, 567)
        self.failUnless(self.api.is_empty())

    def testFailureReason(self):
        # Readable, Type: int
        self.api.enqueue('GET CALL 1234 FAILUREREASON',
                         'CALL 1234 FAILUREREASON 3')
        t = self.obj.FailureReason
        self.assertInstance(t, int)
        self.assertEqual(t, 3)
        self.failUnless(self.api.is_empty())

    def testForwardedBy(self):
        # Readable, Type: str
        self.api.enqueue('GET CALL 1234 FORWARDED_BY',
                         'CALL 1234 FORWARDED_BY eggs')
        t = self.obj.ForwardedBy
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testId(self):
        # Readable, Type: int
        t = self.obj.Id
        self.assertInstance(t, int)
        self.assertEqual(t, 1234)
        self.failUnless(self.api.is_empty())

    def testInputStatus(self):
        # Readable, Type: bool
        self.api.enqueue('GET CALL 1234 VAA_INPUT_STATUS',
                         'CALL 1234 VAA_INPUT_STATUS TRUE')
        t = self.obj.InputStatus
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())

    def testParticipants(self):
        # Readable, Type: ParticipantCollection
        self.api.enqueue('GET CALL 1234 CONF_PARTICIPANTS_COUNT',
                         'CALL 1234 CONF_PARTICIPANTS_COUNT 2')
        self.api.enqueue('GET CALL 1234 CONF_PARTICIPANT 0',
                         'CALL 1234 CONF_PARTICIPANT 0 spam INCOMING_P2P INPROGRESS Spam')
        t = self.obj.Participants
        self.assertInstance(t, ParticipantCollection)
        self.assertEqual(len(t), 2)
        t = t[0].CallType
        self.assertInstance(t, str)
        self.assertEqual(t, 'INCOMING_P2P')
        self.failUnless(self.api.is_empty())

    def testPartnerDisplayName(self):
        # Readable, Type: unicode
        self.api.enqueue('GET CALL 1234 PARTNER_DISPNAME',
                         'CALL 1234 PARTNER_DISPNAME Monty Python')
        t = self.obj.PartnerDisplayName
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'Monty Python')
        self.failUnless(self.api.is_empty())

    def testPartnerHandle(self):
        # Readable, Type: str
        self.api.enqueue('GET CALL 1234 PARTNER_HANDLE',
                         'CALL 1234 PARTNER_HANDLE eggs')
        t = self.obj.PartnerHandle
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testPstnNumber(self):
        # Readable, Type: str
        self.api.enqueue('GET CALL 1234 PSTN_NUMBER',
                         'CALL 1234 PSTN_NUMBER +3712345678')
        t = self.obj.PstnNumber
        self.assertInstance(t, str)
        self.assertEqual(t, '+3712345678')
        self.failUnless(self.api.is_empty())

    def testPstnStatus(self):
        # Readable, Type: unicode
        self.api.enqueue('GET CALL 1234 PSTN_STATUS',
                         'CALL 1234 PSTN_STATUS 6500 PSTN connection creation timeout')
        t = self.obj.PstnStatus
        self.assertInstance(t, unicode)
        self.assertEqual(t, '6500 PSTN connection creation timeout')
        self.failUnless(self.api.is_empty())

    def testRate(self):
        # Readable, Type: int
        self.api.enqueue('GET CALL 1234 RATE',
                         'CALL 1234 RATE 123')
        t = self.obj.Rate
        self.assertInstance(t, int)
        self.assertEqual(t, 123)
        self.failUnless(self.api.is_empty())

    def testRateCurrency(self):
        # Readable, Type: unicode
        self.api.enqueue('GET CALL 1234 RATE_CURRENCY',
                         'CALL 1234 RATE_CURRENCY EUR')
        t = self.obj.RateCurrency
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'EUR')
        self.failUnless(self.api.is_empty())

    def testRatePrecision(self):
        # Readable, Type: int
        self.api.enqueue('GET CALL 1234 RATE_PRECISION',
                         'CALL 1234 RATE_PRECISION 2')
        t = self.obj.RatePrecision
        self.assertInstance(t, int)
        self.assertEqual(t, 2)
        self.failUnless(self.api.is_empty())

    def testRateToText(self):
        # Readable, Type: unicode
        self.api.enqueue('GET CALL 1234 RATE_CURRENCY',
                         'CALL 1234 RATE_CURRENCY EUR')
        self.api.enqueue('GET CALL 1234 RATE',
                         'CALL 1234 RATE 456')
        self.api.enqueue('GET CALL 1234 RATE_PRECISION',
                         'CALL 1234 RATE_PRECISION 2')
        t = self.obj.RateToText
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'EUR 4.560')
        self.failUnless(self.api.is_empty())

    def testRateValue(self):
        # Readable, Type: float
        self.api.enqueue('GET CALL 1234 RATE',
                         'CALL 1234 RATE 456')
        self.api.enqueue('GET CALL 1234 RATE_PRECISION',
                         'CALL 1234 RATE_PRECISION 2')
        t = self.obj.RateValue
        self.assertInstance(t, float)
        self.assertEqual(t, 4.56)
        self.failUnless(self.api.is_empty())

    def testSeen(self):
        # Readable, Writable, Type: bool
        self.api.enqueue('GET CALL 1234 SEEN',
                         'CALL 1234 SEEN FALSE')
        t = self.obj.Seen
        self.assertInstance(t, bool)
        self.assertEqual(t, False)
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET CALL 1234 SEEN TRUE',
                         'CALL 1234 SEEN TRUE')
        self.obj.Seen = True
        self.failUnless(self.api.is_empty())

    def testStatus(self):
        # Readable, Writable, Type: str
        self.api.enqueue('GET CALL 1234 STATUS',
                         'CALL 1234 STATUS INPROGRESS')
        t = self.obj.Status
        self.assertInstance(t, str)
        self.assertEqual(t, 'INPROGRESS')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET CALL 1234 STATUS FINISHED',
                         'CALL 1234 STATUS FINISHED')
        self.obj.Status = 'FINISHED'
        self.failUnless(self.api.is_empty())

    def testSubject(self):
        # Readable, Type: unicode
        self.api.enqueue('GET CALL 1234 SUBJECT',
                         'CALL 1234 SUBJECT eggs')
        t = self.obj.Subject
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testTargetIdentity(self):
        # Readable, Type: str
        self.api.enqueue('GET CALL 1234 TARGET_IDENTITY',
                         'CALL 1234 TARGET_IDENTITY +3712345678')
        t = self.obj.TargetIdentity
        self.assertInstance(t, str)
        self.assertEqual(t, '+3712345678')
        self.failUnless(self.api.is_empty())

    def testTimestamp(self):
        # Readable, Type: float
        self.api.enqueue('GET CALL 1234 TIMESTAMP',
                         'CALL 1234 TIMESTAMP 235.4')
        t = self.obj.Timestamp
        self.assertInstance(t, float)
        self.assertEqual(t, 235.4)
        self.failUnless(self.api.is_empty())

    def testTransferActive(self):
        # Readable, Type: bool
        self.api.enqueue('GET CALL 1234 TRANSFER_ACTIVE',
                         'CALL 1234 TRANSFER_ACTIVE TRUE')
        t = self.obj.TransferActive
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())

    def testTransferredBy(self):
        # Readable, Type: str
        self.api.enqueue('GET CALL 1234 TRANSFERRED_BY',
                         'CALL 1234 TRANSFERRED_BY eggs')
        t = self.obj.TransferredBy
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testTransferredTo(self):
        # Readable, Type: str
        self.api.enqueue('GET CALL 1234 TRANSFERRED_TO',
                         'CALL 1234 TRANSFERRED_TO eggs')
        t = self.obj.TransferredTo
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testTransferStatus(self):
        # Readable, Type: str
        self.api.enqueue('GET CALL 1234 TRANSFER_STATUS',
                         'CALL 1234 TRANSFER_STATUS INPROGRESS')
        t = self.obj.TransferStatus
        self.assertInstance(t, str)
        self.assertEqual(t, 'INPROGRESS')
        self.failUnless(self.api.is_empty())

    def testType(self):
        # Readable, Type: str
        self.api.enqueue('GET CALL 1234 TYPE',
                         'CALL 1234 TYPE eggs')
        t = self.obj.Type
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testVideoReceiveStatus(self):
        # Readable, Type: str
        self.api.enqueue('GET CALL 1234 VIDEO_RECEIVE_STATUS',
                         'CALL 1234 VIDEO_RECEIVE_STATUS eggs')
        t = self.obj.VideoReceiveStatus
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testVideoSendStatus(self):
        # Readable, Type: str
        self.api.enqueue('GET CALL 1234 VIDEO_SEND_STATUS',
                         'CALL 1234 VIDEO_SEND_STATUS eggs')
        t = self.obj.VideoSendStatus
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testVideoStatus(self):
        # Readable, Type: str
        self.api.enqueue('GET CALL 1234 VIDEO_STATUS',
                         'CALL 1234 VIDEO_STATUS VIDEO_NONE')
        t = self.obj.VideoStatus
        self.assertInstance(t, str)
        self.assertEqual(t, 'VIDEO_NONE')
        self.failUnless(self.api.is_empty())

    def testVmAllowedDuration(self):
        # Readable, Type: int
        self.api.enqueue('GET CALL 1234 VM_ALLOWED_DURATION',
                         'CALL 1234 VM_ALLOWED_DURATION 123')
        t = self.obj.VmAllowedDuration
        self.assertInstance(t, int)
        self.assertEqual(t, 123)
        self.failUnless(self.api.is_empty())

    def testVmDuration(self):
        # Readable, Type: int
        self.api.enqueue('GET CALL 1234 VM_DURATION',
                         'CALL 1234 VM_DURATION 123')
        t = self.obj.VmDuration
        self.assertInstance(t, int)
        self.assertEqual(t, 123)
        self.failUnless(self.api.is_empty())


class ParticipantTest(skype4pytest.TestCase):
    def setUpObject(self):
        self.obj = Participant(Call(self.skype, '1234'), 2)

    def enqueueConfParticipant(self):
        self.api.enqueue('GET CALL 1234 CONF_PARTICIPANT 2',
                         'CALL 1234 CONF_PARTICIPANT 2 spam INCOMING_P2P INPROGRESS Monty Python')

    # Properties
    # ==========

    def testCall(self):
        # Readable, Type: Call
        t = self.obj.Call
        self.assertInstance(t, Call)
        self.assertEqual(t.Id, 1234)
        self.failUnless(self.api.is_empty())

    def testCallStatus(self):
        # Readable, Type: str
        self.enqueueConfParticipant()
        t = self.obj.CallStatus
        self.assertInstance(t, str)
        self.assertEqual(t, 'INPROGRESS')
        self.failUnless(self.api.is_empty())

    def testCallType(self):
        # Readable, Type: str
        self.enqueueConfParticipant()
        t = self.obj.CallType
        self.assertInstance(t, str)
        self.assertEqual(t, 'INCOMING_P2P')
        self.failUnless(self.api.is_empty())

    def testDisplayName(self):
        # Readable, Type: unicode
        self.enqueueConfParticipant()
        t = self.obj.DisplayName
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'Monty Python')
        self.failUnless(self.api.is_empty())

    def testHandle(self):
        # Readable, Type: str
        self.enqueueConfParticipant()
        t = self.obj.Handle
        self.assertInstance(t, str)
        self.assertEqual(t, 'spam')
        self.failUnless(self.api.is_empty())

    def testId(self):
        # Readable, Type: int
        t = self.obj.Id
        self.assertInstance(t, int)
        self.assertEqual(t, 1234)
        self.failUnless(self.api.is_empty())

    def testIdx(self):
        # Readable, Type: int
        t = self.obj.Idx
        self.assertInstance(t, int)
        self.assertEqual(t, 2)
        self.failUnless(self.api.is_empty())


class ConferenceTest(skype4pytest.TestCase):
    def setUpObject(self):
        self.obj = Conference(self.skype, '89')

    def enqueueSearchCalls(self, search='CALLS '):
        self.api.enqueue('SEARCH %s' % search,
                         '%s 123, 456' % search)
        self.api.enqueue('GET CALL 123 CONF_ID',
                         'CALL 123 CONF_ID 67')
        self.api.enqueue('GET CALL 456 CONF_ID',
                         'CALL 456 CONF_ID 89')

    # Methods
    # =======

    def testFinish(self):
        self.enqueueSearchCalls()
        self.api.enqueue('ALTER CALL 456 END HANGUP')
        self.obj.Finish()
        self.failUnless(self.api.is_empty())

    def testHold(self):
        self.enqueueSearchCalls()
        self.api.enqueue('ALTER CALL 456 HOLD')
        self.obj.Hold()
        self.failUnless(self.api.is_empty())

    def testResume(self):
        self.enqueueSearchCalls()
        self.api.enqueue('ALTER CALL 456 RESUME')
        self.obj.Resume()
        self.failUnless(self.api.is_empty())

    # Properties
    # ==========

    def testActiveCalls(self):
        # Readable, Type: CallCollection
        self.enqueueSearchCalls('ACTIVECALLS')
        t = self.obj.ActiveCalls
        self.assertInstance(t, CallCollection)
        self.assertEqual(len(t), 1)
        self.failUnless(self.api.is_empty())

    def testCalls(self):
        # Readable, Type: CallCollection
        self.enqueueSearchCalls()
        t = self.obj.Calls
        self.assertInstance(t, CallCollection)
        self.assertEqual(len(t), 1)
        self.failUnless(self.api.is_empty())

    def testId(self):
        # Readable, Type: int
        t = self.obj.Id
        self.assertInstance(t, int)
        self.assertEqual(t, 89)
        self.failUnless(self.api.is_empty())


def suite():
    return unittest.TestSuite([
        unittest.defaultTestLoader.loadTestsFromTestCase(CallTest),
        unittest.defaultTestLoader.loadTestsFromTestCase(ParticipantTest),
        unittest.defaultTestLoader.loadTestsFromTestCase(ConferenceTest),
    ])


if __name__ == '__main__':
    unittest.main()
