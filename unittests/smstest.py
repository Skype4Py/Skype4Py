import unittest

import skype4pytest
from Skype4Py.sms import *


class SmsMessageTest(skype4pytest.TestCase):
    def setUpObject(self):
        self.obj = SmsMessage(self.skype, '1234')

    # Methods
    # =======

    def testDelete(self):
        self.api.enqueue('DELETE SMS 1234')
        self.obj.Delete()
        self.failUnless(self.api.is_empty())

    def testMarkAsSeen(self):
        self.api.enqueue('SET SMS 1234 SEEN',
                         'SMS 1234 STATUS READ')
        self.obj.MarkAsSeen()
        self.failUnless(self.api.is_empty())

    def testSend(self):
        self.api.enqueue('ALTER SMS 1234 SEND')
        self.obj.Send()
        self.failUnless(self.api.is_empty())

    # Properties
    # ==========

    def testBody(self):
        # Readable, Writable, Type: unicode
        self.api.enqueue('GET SMS 1234 BODY',
                         'SMS 1234 BODY eggs')
        t = self.obj.Body
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET SMS 1234 BODY eggs',
                         'SMS 1234 BODY eggs')
        self.obj.Body = 'eggs'
        self.failUnless(self.api.is_empty())

    def testChunks(self):
        # Readable, Type: SmsChunkCollection
        self.api.enqueue('GET SMS 1234 CHUNKING',
                         'SMS 1234 CHUNKING 2 30')
        t = self.obj.Chunks
        self.assertInstance(t, SmsChunkCollection)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())

    def testDatetime(self):
        # Readable, Type: datetime
        from datetime import datetime
        from time import time
        now = time()
        self.api.enqueue('GET SMS 1234 TIMESTAMP',
                         'SMS 1234 TIMESTAMP %f' % now)
        t = self.obj.Datetime
        self.assertInstance(t, datetime)
        self.assertEqual(t, datetime.fromtimestamp(now))
        self.failUnless(self.api.is_empty())

    def testFailureReason(self):
        # Readable, Type: str
        self.api.enqueue('GET SMS 1234 FAILUREREASON',
                         'SMS 1234 FAILUREREASON eggs')
        t = self.obj.FailureReason
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testId(self):
        # Readable, Type: int
        t = self.obj.Id
        self.assertInstance(t, int)
        self.assertEqual(t, 1234)

    def testIsFailedUnseen(self):
        # Readable, Type: bool
        self.api.enqueue('GET SMS 1234 IS_FAILED_UNSEEN',
                         'SMS 1234 IS_FAILED_UNSEEN TRUE')
        t = self.obj.IsFailedUnseen
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())

    def testPrice(self):
        # Readable, Type: int
        self.api.enqueue('GET SMS 1234 PRICE',
                         'SMS 1234 PRICE 123')
        t = self.obj.Price
        self.assertInstance(t, int)
        self.assertEqual(t, 123)
        self.failUnless(self.api.is_empty())

    def testPriceCurrency(self):
        # Readable, Type: unicode
        self.api.enqueue('GET SMS 1234 PRICE_CURRENCY',
                         'SMS 1234 PRICE_CURRENCY EUR')
        t = self.obj.PriceCurrency
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'EUR')
        self.failUnless(self.api.is_empty())

    def testPricePrecision(self):
        # Readable, Type: int
        self.api.enqueue('GET SMS 1234 PRICE_PRECISION',
                         'SMS 1234 PRICE_PRECISION 3')
        t = self.obj.PricePrecision
        self.assertInstance(t, int)
        self.assertEqual(t, 3)
        self.failUnless(self.api.is_empty())

    def testPriceToText(self):
        # Readable, Type: unicode
        self.api.enqueue('GET SMS 1234 PRICE_CURRENCY',
                         'SMS 1234 PRICE_CURRENCY EUR')
        self.api.enqueue('GET SMS 1234 PRICE',
                         'SMS 1234 PRICE 123')
        self.api.enqueue('GET SMS 1234 PRICE_PRECISION',
                         'SMS 1234 PRICE_PRECISION 3')
        t = self.obj.PriceToText
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'EUR 0.123')
        self.failUnless(self.api.is_empty())

    def testPriceValue(self):
        # Readable, Type: float
        self.api.enqueue('GET SMS 1234 PRICE',
                         'SMS 1234 PRICE 123')
        self.api.enqueue('GET SMS 1234 PRICE_PRECISION',
                         'SMS 1234 PRICE_PRECISION 3')
        t = self.obj.PriceValue
        self.assertInstance(t, float)
        self.assertEqual(t, 0.123)
        self.failUnless(self.api.is_empty())

    def testReplyToNumber(self):
        # Readable, Writable, Type: str
        self.api.enqueue('GET SMS 1234 REPLY_TO_NUMBER',
                         'SMS 1234 REPLY_TO_NUMBER eggs')
        t = self.obj.ReplyToNumber
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET SMS 1234 REPLY_TO_NUMBER eggs',
                         'SMS 1234 REPLY_TO_NUMBER eggs')
        self.obj.ReplyToNumber = 'eggs'
        self.failUnless(self.api.is_empty())

    def testSeen(self):
        # Writable, Type: bool
        from warnings import simplefilter
        self.api.enqueue('SET SMS 1234 SEEN',
                         'SMS 1234 STATUS READ')
        simplefilter('ignore')
        try:
            self.obj.Seen = True
        finally:
            simplefilter('default')
        self.failUnless(self.api.is_empty())

    def testStatus(self):
        # Readable, Type: str
        self.api.enqueue('GET SMS 1234 STATUS',
                         'SMS 1234 STATUS RECEIVED')
        t = self.obj.Status
        self.assertInstance(t, str)
        self.assertEqual(t, 'RECEIVED')
        self.failUnless(self.api.is_empty())

    def testTargetNumbers(self):
        # Readable, Writable, Type: tuple of str
        self.api.enqueue('GET SMS 1234 TARGET_NUMBERS',
                         'SMS 1234 TARGET_NUMBERS +3712345678, +3723456789')
        t = self.obj.TargetNumbers
        self.assertInstance(t, tuple)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET SMS 1234 TARGET_NUMBERS +3787654321',
                         'SMS 1234 TARGET_NUMBERS +3787654321')
        self.obj.TargetNumbers = ('+3787654321',)
        self.failUnless(self.api.is_empty())

    def testTargets(self):
        # Readable, Type: SmsTargetCollection
        self.api.enqueue('GET SMS 1234 TARGET_NUMBERS',
                         'SMS 1234 TARGET_NUMBERS +3712345678, +3723456789')
        t = self.obj.Targets
        self.assertInstance(t, SmsTargetCollection)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())

    def testTimestamp(self):
        # Readable, Type: float
        self.api.enqueue('GET SMS 1234 TIMESTAMP',
                         'SMS 1234 TIMESTAMP 123.4')
        t = self.obj.Timestamp
        self.assertInstance(t, float)
        self.assertEqual(t, 123.4)
        self.failUnless(self.api.is_empty())

    def testType(self):
        # Readable, Type: str
        self.api.enqueue('GET SMS 1234 TYPE',
                         'SMS 1234 TYPE INCOMING')
        t = self.obj.Type
        self.assertInstance(t, str)
        self.assertEqual(t, 'INCOMING')
        self.failUnless(self.api.is_empty())


class SmsChunkTest(skype4pytest.TestCase):
    def setUpObject(self):
        self.obj = SmsChunk(SmsMessage(self.skype, '1234'), 1)

    # Properties
    # ==========

    def testCharactersLeft(self):
        # Readable, Type: int
        self.api.enqueue('GET SMS 1234 CHUNKING',
                         'SMS 1234 CHUNKING 2 30')
        t = self.obj.CharactersLeft
        self.assertInstance(t, int)
        self.assertEqual(t, 30)
        self.failUnless(self.api.is_empty())

    def testId(self):
        # Readable, Type: int
        t = self.obj.Id
        self.assertInstance(t, int)
        self.assertEqual(t, 1)

    def testMessage(self):
        # Readable, Type: SmsMessage
        t = self.obj.Message
        self.assertInstance(t, SmsMessage)
        self.assertEqual(t.Id, 1234)

    def testText(self):
        # Readable, Type: unicode
        self.api.enqueue('GET SMS 1234 CHUNK 1',
                         'SMS 1234 CHUNK 1 eggs')
        t = self.obj.Text
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())


class SmsTargetTest(skype4pytest.TestCase):
    def setUpObject(self):
        self.obj = SmsTarget(SmsMessage(self.skype, '1234'), '+3712345678')

    # Properties
    # ==========

    def testMessage(self):
        # Readable, Type: SmsMessage
        t = self.obj.Message
        self.assertInstance(t, SmsMessage)
        self.assertEqual(t.Id, 1234)

    def testNumber(self):
        # Readable, Type: str
        t = self.obj.Number
        self.assertInstance(t, str)
        self.assertEqual(t, '+3712345678')

    def testStatus(self):
        # Readable, Type: str
        self.api.enqueue('GET SMS 1234 TARGET_STATUSES',
                         'SMS 1234 TARGET_STATUSES +3723456789=TARGET_NOT_ROUTABLE, +3712345678=TARGET_ACCEPTABLE')
        t = self.obj.Status
        self.assertInstance(t, str)
        self.assertEqual(t, 'TARGET_ACCEPTABLE')
        self.failUnless(self.api.is_empty())


def suite():
    return unittest.TestSuite([
        unittest.defaultTestLoader.loadTestsFromTestCase(SmsMessageTest),
        unittest.defaultTestLoader.loadTestsFromTestCase(SmsChunkTest),
        unittest.defaultTestLoader.loadTestsFromTestCase(SmsTargetTest),
    ])


if __name__ == '__main__':
    unittest.main()
