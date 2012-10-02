import unittest

import skype4pytest
from Skype4Py.user import *


class UserTest(skype4pytest.TestCase):
    def setUpObject(self):
        self.obj = User(self.skype, 'spam')

    # Methods
    # =======

    def testSaveAvatarToFile(self):
        self.api.enqueue('GET USER spam AVATAR 1 c:\\eggs.jpg',
                         'USER spam AVATAR 1 c:\\eggs.jpg')
        self.obj.SaveAvatarToFile('c:\\eggs.jpg')
        self.failUnless(self.api.is_empty())

    def testSetBuddyStatusPendingAuthorization(self):
        self.api.enqueue('SET USER spam BUDDYSTATUS 2 ',
                         'USER spam BUDDYSTATUS 2')
        self.obj.SetBuddyStatusPendingAuthorization()
        self.failUnless(self.api.is_empty())

    # Properties
    # ==========

    def testAbout(self):
        # Readable, Type: unicode
        self.api.enqueue('GET USER spam ABOUT',
                         'USER spam ABOUT eggs')
        t = self.obj.About
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testAliases(self):
        # Readable, Type: list of str
        self.api.enqueue('GET USER spam ALIASES',
                         'USER spam ALIASES eggs sausage')
        t = self.obj.Aliases
        self.assertInstance(t, list)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())

    def testBirthday(self):
        # Readable, Type: date or None
        from datetime import date
        self.api.enqueue('GET USER spam BIRTHDAY',
                         'USER spam BIRTHDAY 20090101')
        t = self.obj.Birthday
        self.assertInstance(t, date)
        self.assertEqual(t, date(2009, 1, 1))
        self.failUnless(self.api.is_empty())

    def testBuddyStatus(self):
        # Readable, Writable, Type: int
        self.api.enqueue('GET USER spam BUDDYSTATUS',
                         'USER spam BUDDYSTATUS 2')
        t = self.obj.BuddyStatus
        self.assertInstance(t, int)
        self.assertEqual(t, 2)
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET USER spam BUDDYSTATUS 3',
                         'USER spam BUDDYSTATUS 3')
        self.obj.BuddyStatus = 3
        self.failUnless(self.api.is_empty())

    def testCanLeaveVoicemail(self):
        # Readable, Type: bool
        self.api.enqueue('GET USER spam CAN_LEAVE_VM',
                         'USER spam CAN_LEAVE_VM TRUE')
        t = self.obj.CanLeaveVoicemail
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())

    def testCity(self):
        # Readable, Type: unicode
        self.api.enqueue('GET USER spam CITY',
                         'USER spam CITY eggs')
        t = self.obj.City
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testCountry(self):
        # Readable, Type: unicode
        self.api.enqueue('GET USER spam COUNTRY',
                         'USER spam COUNTRY de eggs')
        t = self.obj.Country
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testCountryCode(self):
        # Readable, Type: str
        self.api.enqueue('GET USER spam COUNTRY',
                         'USER spam COUNTRY de eggs')
        t = self.obj.CountryCode
        self.assertInstance(t, str)
        self.assertEqual(t, 'de')
        self.failUnless(self.api.is_empty())

    def testDisplayName(self):
        # Readable, Writable, Type: unicode
        self.api.enqueue('GET USER spam DISPLAYNAME',
                         'USER spam DISPLAYNAME eggs')
        t = self.obj.DisplayName
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET USER spam DISPLAYNAME eggs',
                         'USER spam DISPLAYNAME eggs')
        self.obj.DisplayName = 'eggs'
        self.failUnless(self.api.is_empty())

    def testFullName(self):
        # Readable, Type: unicode
        self.api.enqueue('GET USER spam FULLNAME',
                         'USER spam FULLNAME eggs')
        t = self.obj.FullName
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testHandle(self):
        # Readable, Type: str
        t = self.obj.Handle
        self.assertInstance(t, str)
        self.assertEqual(t, 'spam')

    def testHasCallEquipment(self):
        # Readable, Type: bool
        self.api.enqueue('GET USER spam HASCALLEQUIPMENT',
                         'USER spam HASCALLEQUIPMENT TRUE')
        t = self.obj.HasCallEquipment
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())

    def testHomepage(self):
        # Readable, Type: unicode
        self.api.enqueue('GET USER spam HOMEPAGE',
                         'USER spam HOMEPAGE eggs')
        t = self.obj.Homepage
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testIsAuthorized(self):
        # Readable, Writable, Type: bool
        self.api.enqueue('GET USER spam ISAUTHORIZED',
                         'USER spam ISAUTHORIZED TRUE')
        t = self.obj.IsAuthorized
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET USER spam ISAUTHORIZED FALSE',
                         'USER spam ISAUTHORIZED FALSE')
        self.obj.IsAuthorized = False
        self.failUnless(self.api.is_empty())

    def testIsBlocked(self):
        # Readable, Writable, Type: bool
        self.api.enqueue('GET USER spam ISBLOCKED',
                         'USER spam ISBLOCKED TRUE')
        t = self.obj.IsBlocked
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET USER spam ISBLOCKED FALSE',
                         'USER spam ISBLOCKED FALSE')
        self.obj.IsBlocked = False
        self.failUnless(self.api.is_empty())

    def testIsCallForwardActive(self):
        # Readable, Type: bool
        self.api.enqueue('GET USER spam IS_CF_ACTIVE',
                         'USER spam IS_CF_ACTIVE TRUE')
        t = self.obj.IsCallForwardActive
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())

    def testIsSkypeOutContact(self):
        # Readable, Type: bool
        self.api.enqueue('GET USER spam ONLINESTATUS',
                         'USER spam ONLINESTATUS SKYPEOUT')
        t = self.obj.IsSkypeOutContact
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())

    def testIsVideoCapable(self):
        # Readable, Type: bool
        self.api.enqueue('GET USER spam IS_VIDEO_CAPABLE',
                         'USER spam IS_VIDEO_CAPABLE TRUE')
        t = self.obj.IsVideoCapable
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())

    def testIsVoicemailCapable(self):
        # Readable, Type: bool
        self.api.enqueue('GET USER spam IS_VOICEMAIL_CAPABLE',
                         'USER spam IS_VOICEMAIL_CAPABLE TRUE')
        t = self.obj.IsVoicemailCapable
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())

    def testLanguage(self):
        # Readable, Type: unicode
        self.api.enqueue('GET USER spam LANGUAGE',
                         'USER spam LANGUAGE de eggs')
        t = self.obj.Language
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testLanguageCode(self):
        # Readable, Type: str
        self.api.enqueue('GET USER spam LANGUAGE',
                         'USER spam LANGUAGE de eggs')
        t = self.obj.LanguageCode
        self.assertInstance(t, str)
        self.assertEqual(t, 'de')
        self.failUnless(self.api.is_empty())

    def testLastOnline(self):
        # Readable, Type: float
        self.api.enqueue('GET USER spam LASTONLINETIMESTAMP',
                         'USER spam LASTONLINETIMESTAMP 123.4')
        t = self.obj.LastOnline
        self.assertInstance(t, float)
        self.assertEqual(t, 123.4)
        self.failUnless(self.api.is_empty())

    def testLastOnlineDatetime(self):
        # Readable, Type: datetime
        from datetime import datetime
        from time import time
        now = time()
        self.api.enqueue('GET USER spam LASTONLINETIMESTAMP',
                         'USER spam LASTONLINETIMESTAMP %f' % now)
        t = self.obj.LastOnlineDatetime
        self.assertInstance(t, datetime)
        self.assertEqual(t, datetime.fromtimestamp(now))
        self.failUnless(self.api.is_empty())

    def testMoodText(self):
        # Readable, Type: unicode
        self.api.enqueue('GET USER spam MOOD_TEXT',
                         'USER spam MOOD_TEXT eggs')
        t = self.obj.MoodText
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testNumberOfAuthBuddies(self):
        # Readable, Type: int
        self.api.enqueue('GET USER spam NROF_AUTHED_BUDDIES',
                         'USER spam NROF_AUTHED_BUDDIES 12')
        t = self.obj.NumberOfAuthBuddies
        self.assertInstance(t, int)
        self.assertEqual(t, 12)
        self.failUnless(self.api.is_empty())

    def testOnlineStatus(self):
        # Readable, Type: str
        self.api.enqueue('GET USER spam ONLINESTATUS',
                         'USER spam ONLINESTATUS AWAY')
        t = self.obj.OnlineStatus
        self.assertInstance(t, str)
        self.assertEqual(t, 'AWAY')
        self.failUnless(self.api.is_empty())

    def testPhoneHome(self):
        # Readable, Type: unicode
        self.api.enqueue('GET USER spam PHONE_HOME',
                         'USER spam PHONE_HOME eggs')
        t = self.obj.PhoneHome
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testPhoneMobile(self):
        # Readable, Type: unicode
        self.api.enqueue('GET USER spam PHONE_MOBILE',
                         'USER spam PHONE_MOBILE eggs')
        t = self.obj.PhoneMobile
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testPhoneOffice(self):
        # Readable, Type: unicode
        self.api.enqueue('GET USER spam PHONE_OFFICE',
                         'USER spam PHONE_OFFICE eggs')
        t = self.obj.PhoneOffice
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testProvince(self):
        # Readable, Type: unicode
        self.api.enqueue('GET USER spam PROVINCE',
                         'USER spam PROVINCE eggs')
        t = self.obj.Province
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testReceivedAuthRequest(self):
        # Readable, Type: unicode
        self.api.enqueue('GET USER spam RECEIVEDAUTHREQUEST',
                         'USER spam RECEIVEDAUTHREQUEST eggs')
        t = self.obj.ReceivedAuthRequest
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testRichMoodText(self):
        # Readable, Type: unicode
        self.api.enqueue('GET USER spam RICH_MOOD_TEXT',
                         'USER spam RICH_MOOD_TEXT eggs')
        t = self.obj.RichMoodText
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testSex(self):
        # Readable, Type: str
        self.api.enqueue('GET USER spam SEX',
                         'USER spam SEX MALE')
        t = self.obj.Sex
        self.assertInstance(t, str)
        self.assertEqual(t, 'MALE')
        self.failUnless(self.api.is_empty())

    def testSpeedDial(self):
        # Readable, Writable, Type: unicode
        self.api.enqueue('GET USER spam SPEEDDIAL',
                         'USER spam SPEEDDIAL 5')
        t = self.obj.SpeedDial
        self.assertInstance(t, unicode)
        self.assertEqual(t, '5')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET USER spam SPEEDDIAL 6',
                         'USER spam SPEEDDIAL 6')
        self.obj.SpeedDial = '6'
        self.failUnless(self.api.is_empty())

    def testTimezone(self):
        # Readable, Type: int
        self.api.enqueue('GET USER spam TIMEZONE',
                         'USER spam TIMEZONE 86400')
        t = self.obj.Timezone
        self.assertInstance(t, int)
        self.assertEqual(t, 86400)
        self.failUnless(self.api.is_empty())


class GroupTest(skype4pytest.TestCase):
    def setUpObject(self):
        self.obj = Group(self.skype, '1234')

    # Methods
    # =======

    def testAccept(self):
        self.api.enqueue('ALTER GROUP 1234 ACCEPT')
        self.obj.Accept()
        self.failUnless(self.api.is_empty())

    def testAddUser(self):
        self.api.enqueue('ALTER GROUP 1234 ADDUSER spam')
        self.obj.AddUser('spam')
        self.failUnless(self.api.is_empty())

    def testDecline(self):
        self.api.enqueue('ALTER GROUP 1234 DECLINE')
        self.obj.Decline()
        self.failUnless(self.api.is_empty())

    def testRemoveUser(self):
        self.api.enqueue('ALTER GROUP 1234 REMOVEUSER spam')
        self.obj.RemoveUser('spam')
        self.failUnless(self.api.is_empty())

    def testShare(self):
        self.api.enqueue('ALTER GROUP 1234 SHARE spam')
        self.obj.Share('spam')
        self.failUnless(self.api.is_empty())

    # Properties
    # ==========

    def testCustomGroupId(self):
        # Readable, Type: str
        self.api.enqueue('GET GROUP 1234 CUSTOM_GROUP_ID',
                         'GROUP 1234 CUSTOM_GROUP_ID spam')
        t = self.obj.CustomGroupId
        self.assertInstance(t, str)
        self.assertEqual(t, 'spam')
        self.failUnless(self.api.is_empty())

    def testDisplayName(self):
        # Readable, Writable, Type: unicode
        self.api.enqueue('GET GROUP 1234 DISPLAYNAME',
                         'GROUP 1234 DISPLAYNAME eggs')
        t = self.obj.DisplayName
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET GROUP 1234 DISPLAYNAME eggs',
                         'GROUP 1234 DISPLAYNAME eggs')
        self.obj.DisplayName = 'eggs'
        self.failUnless(self.api.is_empty())

    def testId(self):
        # Readable, Type: int
        t = self.obj.Id
        self.assertInstance(t, int)
        self.assertEqual(t, 1234)

    def testIsExpanded(self):
        # Readable, Type: bool
        self.api.enqueue('GET GROUP 1234 EXPANDED',
                         'GROUP 1234 EXPANDED TRUE')
        t = self.obj.IsExpanded
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())

    def testIsVisible(self):
        # Readable, Type: bool
        self.api.enqueue('GET GROUP 1234 VISIBLE',
                         'GROUP 1234 VISIBLE TRUE')
        t = self.obj.IsVisible
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())

    def testOnlineUsers(self):
        # Readable, Type: UserCollection
        self.api.enqueue('GET GROUP 1234 USERS',
                         'GROUP 1234 USERS spam, eggs')
        self.api.enqueue('GET USER spam ONLINESTATUS',
                         'USER spam ONLINESTATUS OFFLINE')
        self.api.enqueue('GET USER eggs ONLINESTATUS',
                         'USER eggs ONLINESTATUS ONLINE')
        t = self.obj.OnlineUsers
        self.assertInstance(t, UserCollection)
        self.assertEqual(len(t), 1)
        self.failUnless(self.api.is_empty())

    def testType(self):
        # Readable, Type: str
        self.api.enqueue('GET GROUP 1234 TYPE',
                         'GROUP 1234 TYPE CUSTOM')
        t = self.obj.Type
        self.assertInstance(t, str)
        self.assertEqual(t, 'CUSTOM')
        self.failUnless(self.api.is_empty())

    def testUsers(self):
        # Readable, Type: UserCollection
        self.api.enqueue('GET GROUP 1234 USERS',
                         'GROUP 1234 USERS spam, eggs')
        t = self.obj.Users
        self.assertInstance(t, UserCollection)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())


def suite():
    return unittest.TestSuite([
        unittest.defaultTestLoader.loadTestsFromTestCase(UserTest),
        unittest.defaultTestLoader.loadTestsFromTestCase(GroupTest),
    ])


if __name__ == '__main__':
    unittest.main()
