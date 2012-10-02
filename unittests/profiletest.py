import unittest

import skype4pytest
from Skype4Py.profile import *


class ProfileTest(skype4pytest.TestCase):
    def setUpObject(self):
        self.obj = self.skype.CurrentUserProfile

    # Properties
    # ==========

    def testAbout(self):
        # Readable, Writable, Type: unicode
        self.api.enqueue('GET PROFILE ABOUT',
                         'PROFILE ABOUT eggs')
        t = self.obj.About
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET PROFILE ABOUT eggs',
                         'PROFILE ABOUT eggs')
        self.obj.About = 'eggs'
        self.failUnless(self.api.is_empty())

    def testBalance(self):
        # Readable, Type: int
        self.api.enqueue('GET PROFILE PSTN_BALANCE',
                         'PROFILE PSTN_BALANCE 1234')
        t = self.obj.Balance
        self.assertInstance(t, int)
        self.assertEqual(t, 1234)
        self.failUnless(self.api.is_empty())

    def testBalanceCurrency(self):
        # Readable, Type: unicode
        self.api.enqueue('GET PROFILE PSTN_BALANCE_CURRENCY',
                         'PROFILE PSTN_BALANCE_CURRENCY EUR')
        t = self.obj.BalanceCurrency
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'EUR')
        self.failUnless(self.api.is_empty())

    def testBalanceToText(self):
        # Readable, Type: unicode
        self.api.enqueue('GET PROFILE PSTN_BALANCE_CURRENCY',
                         'PROFILE PSTN_BALANCE_CURRENCY EUR')
        self.api.enqueue('GET PROFILE PSTN_BALANCE',
                         'PROFILE PSTN_BALANCE 1234')
        t = self.obj.BalanceToText
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'EUR 12.34')
        self.failUnless(self.api.is_empty())

    def testBalanceValue(self):
        # Readable, Type: float
        self.api.enqueue('GET PROFILE PSTN_BALANCE',
                         'PROFILE PSTN_BALANCE 1234')
        t = self.obj.BalanceValue
        self.assertInstance(t, float)
        self.assertEqual(t, 12.34)
        self.failUnless(self.api.is_empty())

    def testBirthday(self):
        # Readable, Writable, Type: date
        from datetime import date
        self.api.enqueue('GET PROFILE BIRTHDAY',
                         'PROFILE BIRTHDAY 20090101')
        t = self.obj.Birthday
        self.assertInstance(t, date)
        self.assertEqual(t, date(2009, 1, 1))
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET PROFILE BIRTHDAY 20090201',
                         'PROFILE BIRTHDAY 20090201')
        self.obj.Birthday = date(2009, 2, 1)
        self.failUnless(self.api.is_empty())

    def testCallApplyCF(self):
        # Readable, Writable, Type: bool
        self.api.enqueue('GET PROFILE CALL_APPLY_CF',
                         'PROFILE CALL_APPLY_CF TRUE')
        t = self.obj.CallApplyCF
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET PROFILE CALL_APPLY_CF FALSE',
                         'PROFILE CALL_APPLY_CF FALSE')
        self.obj.CallApplyCF = False
        self.failUnless(self.api.is_empty())

    def testCallForwardRules(self):
        # Readable, Writable, Type: str
        self.api.enqueue('GET PROFILE CALL_FORWARD_RULES',
                         'PROFILE CALL_FORWARD_RULES eggs')
        t = self.obj.CallForwardRules
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET PROFILE CALL_FORWARD_RULES eggs',
                         'PROFILE CALL_FORWARD_RULES eggs')
        self.obj.CallForwardRules = 'eggs'
        self.failUnless(self.api.is_empty())

    def testCallNoAnswerTimeout(self):
        # Readable, Writable, Type: int
        self.api.enqueue('GET PROFILE CALL_NOANSWER_TIMEOUT',
                         'PROFILE CALL_NOANSWER_TIMEOUT 123')
        t = self.obj.CallNoAnswerTimeout
        self.assertInstance(t, int)
        self.assertEqual(t, 123)
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET PROFILE CALL_NOANSWER_TIMEOUT 14',
                         'PROFILE CALL_NOANSWER_TIMEOUT 14')
        self.obj.CallNoAnswerTimeout = 14
        self.failUnless(self.api.is_empty())

    def testCallSendToVM(self):
        # Readable, Writable, Type: bool
        self.api.enqueue('GET PROFILE CALL_SEND_TO_VM',
                         'PROFILE CALL_SEND_TO_VM TRUE')
        t = self.obj.CallSendToVM
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET PROFILE CALL_SEND_TO_VM FALSE',
                         'PROFILE CALL_SEND_TO_VM FALSE')
        self.obj.CallSendToVM = False
        self.failUnless(self.api.is_empty())

    def testCity(self):
        # Readable, Writable, Type: unicode
        self.api.enqueue('GET PROFILE CITY',
                         'PROFILE CITY eggs')
        t = self.obj.City
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET PROFILE CITY eggs',
                         'PROFILE CITY eggs')
        self.obj.City = 'eggs'
        self.failUnless(self.api.is_empty())

    def testCountry(self):
        # Readable, Writable, Type: unicode
        self.api.enqueue('GET PROFILE COUNTRY',
                         'PROFILE COUNTRY eggs')
        t = self.obj.Country
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET PROFILE COUNTRY eggs',
                         'PROFILE COUNTRY eggs')
        self.obj.Country = 'eggs'
        self.failUnless(self.api.is_empty())

    def testFullName(self):
        # Readable, Writable, Type: unicode
        self.api.enqueue('GET PROFILE FULLNAME',
                         'PROFILE FULLNAME eggs')
        t = self.obj.FullName
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET PROFILE FULLNAME eggs',
                         'PROFILE FULLNAME eggs')
        self.obj.FullName = 'eggs'
        self.failUnless(self.api.is_empty())

    def testHomepage(self):
        # Readable, Writable, Type: unicode
        self.api.enqueue('GET PROFILE HOMEPAGE',
                         'PROFILE HOMEPAGE eggs')
        t = self.obj.Homepage
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET PROFILE HOMEPAGE eggs',
                         'PROFILE HOMEPAGE eggs')
        self.obj.Homepage = 'eggs'
        self.failUnless(self.api.is_empty())

    def testIPCountry(self):
        # Readable, Type: str
        self.api.enqueue('GET PROFILE IPCOUNTRY',
                         'PROFILE IPCOUNTRY de')
        t = self.obj.IPCountry
        self.assertInstance(t, str)
        self.assertEqual(t, 'de')
        self.failUnless(self.api.is_empty())

    def testLanguages(self):
        # Readable, Writable, Type: list of str
        self.api.enqueue('GET PROFILE LANGUAGES',
                         'PROFILE LANGUAGES en de')
        t = self.obj.Languages
        self.assertInstance(t, list)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET PROFILE LANGUAGES en de',
                         'PROFILE LANGUAGES en de')
        self.obj.Languages = ['en', 'de']
        self.failUnless(self.api.is_empty())

    def testMoodText(self):
        # Readable, Writable, Type: unicode
        self.api.enqueue('GET PROFILE MOOD_TEXT',
                         'PROFILE MOOD_TEXT eggs')
        t = self.obj.MoodText
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET PROFILE MOOD_TEXT eggs',
                         'PROFILE MOOD_TEXT eggs')
        self.obj.MoodText = 'eggs'
        self.failUnless(self.api.is_empty())

    def testPhoneHome(self):
        # Readable, Writable, Type: unicode
        self.api.enqueue('GET PROFILE PHONE_HOME',
                         'PROFILE PHONE_HOME eggs')
        t = self.obj.PhoneHome
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET PROFILE PHONE_HOME eggs',
                         'PROFILE PHONE_HOME eggs')
        self.obj.PhoneHome = 'eggs'
        self.failUnless(self.api.is_empty())

    def testPhoneMobile(self):
        # Readable, Writable, Type: unicode
        self.api.enqueue('GET PROFILE PHONE_MOBILE',
                         'PROFILE PHONE_MOBILE eggs')
        t = self.obj.PhoneMobile
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET PROFILE PHONE_MOBILE eggs',
                         'PROFILE PHONE_MOBILE eggs')
        self.obj.PhoneMobile = 'eggs'
        self.failUnless(self.api.is_empty())

    def testPhoneOffice(self):
        # Readable, Writable, Type: unicode
        self.api.enqueue('GET PROFILE PHONE_OFFICE',
                         'PROFILE PHONE_OFFICE eggs')
        t = self.obj.PhoneOffice
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET PROFILE PHONE_OFFICE eggs',
                         'PROFILE PHONE_OFFICE eggs')
        self.obj.PhoneOffice = 'eggs'
        self.failUnless(self.api.is_empty())

    def testProvince(self):
        # Readable, Writable, Type: unicode
        self.api.enqueue('GET PROFILE PROVINCE',
                         'PROFILE PROVINCE eggs')
        t = self.obj.Province
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET PROFILE PROVINCE eggs',
                         'PROFILE PROVINCE eggs')
        self.obj.Province = 'eggs'
        self.failUnless(self.api.is_empty())

    def testRichMoodText(self):
        # Readable, Writable, Type: unicode
        self.api.enqueue('GET PROFILE RICH_MOOD_TEXT',
                         'PROFILE RICH_MOOD_TEXT eggs')
        t = self.obj.RichMoodText
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET PROFILE RICH_MOOD_TEXT eggs',
                         'PROFILE RICH_MOOD_TEXT eggs')
        self.obj.RichMoodText = 'eggs'
        self.failUnless(self.api.is_empty())

    def testSex(self):
        # Readable, Writable, Type: str
        self.api.enqueue('GET PROFILE SEX',
                         'PROFILE SEX MALE')
        t = self.obj.Sex
        self.assertInstance(t, str)
        self.assertEqual(t, 'MALE')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET PROFILE SEX FEMALE',
                         'PROFILE SEX FEMALE')
        self.obj.Sex = 'FEMALE'
        self.failUnless(self.api.is_empty())

    def testTimezone(self):
        # Readable, Writable, Type: int
        self.api.enqueue('GET PROFILE TIMEZONE',
                         'PROFILE TIMEZONE 86400')
        t = self.obj.Timezone
        self.assertInstance(t, int)
        self.assertEqual(t, 86400)
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET PROFILE TIMEZONE 90000',
                         'PROFILE TIMEZONE 90000')
        self.obj.Timezone = 90000
        self.failUnless(self.api.is_empty())

    def testValidatedSmsNumbers(self):
        # Readable, Type: list of str
        self.api.enqueue('GET PROFILE SMS_VALIDATED_NUMBERS',
                         'PROFILE SMS_VALIDATED_NUMBERS +3712345678, +3723456789')
        t = self.obj.ValidatedSmsNumbers
        self.assertInstance(t, list)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())


def suite():
    return unittest.TestSuite([
        unittest.defaultTestLoader.loadTestsFromTestCase(ProfileTest),
    ])


if __name__ == '__main__':
    unittest.main()
