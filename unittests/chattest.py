import unittest

import skype4pytest
from Skype4Py.chat import *


class ChatTest(skype4pytest.TestCase):
    def setUpObject(self):
        self.obj = Chat(self.skype, 'spam')

    # Methods
    # =======

    def testAcceptAdd(self):
        self.api.enqueue('ALTER CHAT spam ACCEPTADD')
        self.obj.AcceptAdd()
        self.failUnless(self.api.is_empty())

    def testAddMembers(self):
        self.api.enqueue('ALTER CHAT spam ADDMEMBERS eggs')
        self.obj.AddMembers(User(self.skype, 'eggs'))
        self.failUnless(self.api.is_empty())

    def testBookmark(self):
        self.api.enqueue('ALTER CHAT spam BOOKMARK')
        self.obj.Bookmark()
        self.failUnless(self.api.is_empty())

    def testClearRecentMessages(self):
        self.api.enqueue('ALTER CHAT spam CLEARRECENTMESSAGES')
        self.obj.ClearRecentMessages()
        self.failUnless(self.api.is_empty())

    def testDisband(self):
        self.api.enqueue('ALTER CHAT spam DISBAND')
        self.obj.Disband()
        self.failUnless(self.api.is_empty())

    def testEnterPassword(self):
        self.api.enqueue('ALTER CHAT spam ENTERPASSWORD eggs')
        self.obj.EnterPassword('eggs')
        self.failUnless(self.api.is_empty())

    def testJoin(self):
        self.api.enqueue('ALTER CHAT spam JOIN')
        self.obj.Join()
        self.failUnless(self.api.is_empty())

    def testKick(self):
        self.api.enqueue('ALTER CHAT spam KICK eggs, sausage')
        self.obj.Kick('eggs', 'sausage')
        self.failUnless(self.api.is_empty())

    def _testKickBan(self):
        self.api.enqueue('ALTER CHAT spam KICKBAN eggs, sausage')
        self.obj.KickBan('eggs', 'sausage')
        self.failUnless(self.api.is_empty())

    def testLeave(self):
        self.api.enqueue('ALTER CHAT spam LEAVE')
        self.obj.Leave()
        self.failUnless(self.api.is_empty())

    def testOpenWindow(self):
        self.api.enqueue('OPEN CHAT spam')
        self.obj.OpenWindow()
        self.failUnless(self.api.is_empty())

    def testSendMessage(self):
        # Returned type: ChatMessage
        self.api.enqueue('CHATMESSAGE spam eggs',
                         'CHATMESSAGE 345 STATUS SENDING')
        t = self.obj.SendMessage('eggs')
        self.assertInstance(t, ChatMessage)
        self.assertEqual(t.Id, 345)
        self.failUnless(self.api.is_empty())

    def testSetPassword(self):
        self.api.enqueue('ALTER CHAT spam SETPASSWORD eggs sausage')
        self.obj.SetPassword('eggs', 'sausage')
        self.failUnless(self.api.is_empty())

    def testUnbookmark(self):
        self.api.enqueue('ALTER CHAT spam UNBOOKMARK')
        self.obj.Unbookmark()
        self.failUnless(self.api.is_empty())

    # Properties
    # ==========

    def testActiveMembers(self):
        # Readable, Type: UserCollection
        self.api.enqueue('GET CHAT spam ACTIVEMEMBERS',
                         'CHAT spam ACTIVEMEMBERS eggs sausage')
        t = self.obj.ActiveMembers
        self.assertInstance(t, UserCollection)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())

    def testActivityDatetime(self):
        # Readable, Type: datetime
        from datetime import datetime
        from time import time
        now = time()
        self.api.enqueue('GET CHAT spam ACTIVITY_TIMESTAMP',
                         'CHAT spam ACTIVITY_TIMESTAMP %f' % now)
        t = self.obj.ActivityDatetime
        self.assertInstance(t, datetime)
        self.assertEqual(t, datetime.fromtimestamp(now))
        self.failUnless(self.api.is_empty())

    def testActivityTimestamp(self):
        # Readable, Type: float
        self.api.enqueue('GET CHAT spam ACTIVITY_TIMESTAMP',
                         'CHAT spam ACTIVITY_TIMESTAMP 123.4')
        t = self.obj.ActivityTimestamp
        self.assertInstance(t, float)
        self.assertEqual(t, 123.4)
        self.failUnless(self.api.is_empty())

    def testAdder(self):
        # Readable, Type: User
        self.api.enqueue('GET CHAT spam ADDER',
                         'CHAT spam ADDER eggs')
        t = self.obj.Adder
        self.assertInstance(t, User)
        self.assertEqual(t.Handle, 'eggs')
        self.failUnless(self.api.is_empty())

    def testAlertString(self):
        # Writable, Type: unicode
        self.api.enqueue('ALTER CHAT spam SETALERTSTRING =eggs')
        self.obj.AlertString = 'eggs'
        self.failUnless(self.api.is_empty())

    def testApplicants(self):
        # Readable, Type: UserCollection
        self.api.enqueue('GET CHAT spam APPLICANTS',
                         'CHAT spam APPLICANTS eggs, sausage')
        t = self.obj.Applicants
        self.assertInstance(t, UserCollection)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())

    def testBlob(self):
        # Readable, Type: str
        self.api.enqueue('GET CHAT spam BLOB',
                         'CHAT spam BLOB eggs')
        t = self.obj.Blob
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testBookmarked(self):
        # Readable, Type: bool
        self.api.enqueue('GET CHAT spam BOOKMARKED',
                         'CHAT spam BOOKMARKED TRUE')
        t = self.obj.Bookmarked
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())

    def testDatetime(self):
        # Readable, Type: datetime
        from datetime import datetime
        from time import time
        now = time()
        self.api.enqueue('GET CHAT spam TIMESTAMP',
                         'CHAT spam TIMESTAMP %f' % now)
        t = self.obj.Datetime
        self.assertInstance(t, datetime)
        self.assertEqual(t, datetime.fromtimestamp(now))
        self.failUnless(self.api.is_empty())

    def testDescription(self):
        # Readable, Writable, Type: unicode
        self.api.enqueue('GET CHAT spam DESCRIPTION',
                         'CHAT spam DESCRIPTION eggs')
        t = self.obj.Description
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET CHAT spam DESCRIPTION eggs',
                         'CHAT spam DESCRIPTION eggs')
        self.obj.Description = 'eggs'
        self.failUnless(self.api.is_empty())

    def testDialogPartner(self):
        # Readable, Type: str
        self.api.enqueue('GET CHAT spam DIALOG_PARTNER',
                         'CHAT spam DIALOG_PARTNER eggs')
        t = self.obj.DialogPartner
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testFriendlyName(self):
        # Readable, Type: unicode
        self.api.enqueue('GET CHAT spam FRIENDLYNAME',
                         'CHAT spam FRIENDLYNAME eggs')
        t = self.obj.FriendlyName
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testGuideLines(self):
        # Readable, Writable, Type: unicode
        self.api.enqueue('GET CHAT spam GUIDELINES',
                         'CHAT spam GUIDELINES eggs')
        t = self.obj.GuideLines
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('ALTER CHAT spam SETGUIDELINES eggs')
        self.obj.GuideLines = 'eggs'
        self.failUnless(self.api.is_empty())

    def testMemberObjects(self):
        # Readable, Type: ChatMemberCollection
        self.api.enqueue('GET CHAT spam MEMBEROBJECTS',
                         'CHAT spam MEMBEROBJECTS 67, 89')
        t = self.obj.MemberObjects
        self.assertInstance(t, ChatMemberCollection)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())

    def testMembers(self):
        # Readable, Type: UserCollection
        self.api.enqueue('GET CHAT spam MEMBERS',
                         'CHAT spam MEMBERS eggs sausage')
        t = self.obj.Members
        self.assertInstance(t, UserCollection)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())

    def testMessages(self):
        # Readable, Type: ChatMessageCollection
        self.api.enqueue('GET CHAT spam CHATMESSAGES',
                         'CHAT spam CHATMESSAGES 67, 89')
        t = self.obj.Messages
        self.assertInstance(t, ChatMessageCollection)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())

    def testMyRole(self):
        # Readable, Type: str
        self.api.enqueue('GET CHAT spam MYROLE',
                         'CHAT spam MYROLE eggs')
        t = self.obj.MyRole
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testMyStatus(self):
        # Readable, Type: str
        self.api.enqueue('GET CHAT spam MYSTATUS',
                         'CHAT spam MYSTATUS eggs')
        t = self.obj.MyStatus
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testName(self):
        # Readable, Type: str
        t = self.obj.Name
        self.assertInstance(t, str)
        self.assertEqual(t, 'spam')
        self.failUnless(self.api.is_empty())

    def testOptions(self):
        # Readable, Writable, Type: int
        self.api.enqueue('GET CHAT spam OPTIONS',
                         'CHAT spam OPTIONS 123')
        t = self.obj.Options
        self.assertInstance(t, int)
        self.assertEqual(t, 123)
        self.failUnless(self.api.is_empty())
        self.api.enqueue('ALTER CHAT spam SETOPTIONS eggs')
        self.obj.Options = 'eggs'
        self.failUnless(self.api.is_empty())

    def testPasswordHint(self):
        # Readable, Type: unicode
        self.api.enqueue('GET CHAT spam PASSWORDHINT',
                         'CHAT spam PASSWORDHINT eggs')
        t = self.obj.PasswordHint
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testPosters(self):
        # Readable, Type: UserCollection
        self.api.enqueue('GET CHAT spam POSTERS',
                         'CHAT spam POSTERS eggs, sausage')
        t = self.obj.Posters
        self.assertInstance(t, UserCollection)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())

    def testRecentMessages(self):
        # Readable, Type: ChatMessageCollection
        self.api.enqueue('GET CHAT spam RECENTCHATMESSAGES',
                         'CHAT spam RECENTCHATMESSAGES 67, 89')
        t = self.obj.RecentMessages
        self.assertInstance(t, ChatMessageCollection)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())

    def testStatus(self):
        # Readable, Type: str
        self.api.enqueue('GET CHAT spam STATUS',
                         'CHAT spam STATUS eggs')
        t = self.obj.Status
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testTimestamp(self):
        # Readable, Type: float
        self.api.enqueue('GET CHAT spam TIMESTAMP',
                         'CHAT spam TIMESTAMP 123.4')
        t = self.obj.Timestamp
        self.assertInstance(t, float)
        self.assertEqual(t, 123.4)
        self.failUnless(self.api.is_empty())

    def testTopic(self):
        # Readable, Writable, Type: unicode
        self.api.enqueue('GET CHAT spam TOPIC',
                         'CHAT spam TOPIC eggs')
        t = self.obj.Topic
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('ALTER CHAT spam SETTOPIC eggs')
        self.obj.Topic = 'eggs'
        self.failUnless(self.api.is_empty())

    def testTopicXML(self):
        # Readable, Writable, Type: unicode
        self.api.enqueue('GET CHAT spam TOPICXML',
                         'CHAT spam TOPICXML eggs')
        t = self.obj.TopicXML
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('ALTER CHAT spam SETTOPICXML eggs')
        self.obj.TopicXML = 'eggs'
        self.failUnless(self.api.is_empty())

    def testType(self):
        # Readable, Type: str
        self.api.enqueue('GET CHAT spam TYPE',
                         'CHAT spam TYPE eggs')
        t = self.obj.Type
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())


class ChatMessageTest(skype4pytest.TestCase):
    def setUpObject(self):
        self.obj = ChatMessage(self.skype, '1234')

    # Methods
    # =======

    def testMarkAsSeen(self):
        self.api.enqueue('SET CHATMESSAGE 1234 SEEN',
                         'CHATMESSAGE 1234 STATUS READ')
        self.obj.MarkAsSeen()
        self.failUnless(self.api.is_empty())

    # Properties
    # ==========

    def testBody(self):
        # Readable, Writable, Type: unicode
        self.api.enqueue('GET CHATMESSAGE 1234 BODY',
                         'CHATMESSAGE 1234 BODY eggs')
        t = self.obj.Body
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET CHATMESSAGE 1234 BODY eggs',
                         'CHATMESSAGE 1234 BODY eggs')
        self.obj.Body = 'eggs'
        self.failUnless(self.api.is_empty())

    def testChat(self):
        # Readable, Type: Chat
        self.api.enqueue('GET CHATMESSAGE 1234 CHATNAME',
                         'CHATMESSAGE 1234 CHATNAME spam')
        t = self.obj.Chat
        self.assertInstance(t, Chat)
        self.assertEqual(t.Name, 'spam')
        self.failUnless(self.api.is_empty())

    def testChatName(self):
        # Readable, Type: str
        self.api.enqueue('GET CHATMESSAGE 1234 CHATNAME',
                         'CHATMESSAGE 1234 CHATNAME spam')
        t = self.obj.ChatName
        self.assertInstance(t, str)
        self.assertEqual(t, 'spam')
        self.failUnless(self.api.is_empty())

    def testDatetime(self):
        # Readable, Type: datetime
        from datetime import datetime
        from time import time
        now = time()
        self.api.enqueue('GET CHATMESSAGE 1234 TIMESTAMP',
                         'CHATMESSAGE 1234 TIMESTAMP %f' % now)
        t = self.obj.Datetime
        self.assertInstance(t, datetime)
        self.assertEqual(t, datetime.fromtimestamp(now))
        self.failUnless(self.api.is_empty())

    def testEditedBy(self):
        # Readable, Type: str
        self.api.enqueue('GET CHATMESSAGE 1234 EDITED_BY',
                         'CHATMESSAGE 1234 EDITED_BY eggs')
        t = self.obj.EditedBy
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testEditedDatetime(self):
        # Readable, Type: datetime
        from datetime import datetime
        from time import time
        now = time()
        self.api.enqueue('GET CHATMESSAGE 1234 EDITED_TIMESTAMP',
                         'CHATMESSAGE 1234 EDITED_TIMESTAMP %f' % now)
        t = self.obj.EditedDatetime
        self.assertInstance(t, datetime)
        self.assertEqual(t, datetime.fromtimestamp(now))
        self.failUnless(self.api.is_empty())

    def testEditedTimestamp(self):
        # Readable, Type: float
        self.api.enqueue('GET CHATMESSAGE 1234 EDITED_TIMESTAMP',
                         'CHATMESSAGE 1234 EDITED_TIMESTAMP 123.4')
        t = self.obj.EditedTimestamp
        self.assertInstance(t, float)
        self.assertEqual(t, 123.4)
        self.failUnless(self.api.is_empty())

    def testFromDisplayName(self):
        # Readable, Type: unicode
        self.api.enqueue('GET CHATMESSAGE 1234 FROM_DISPNAME',
                         'CHATMESSAGE 1234 FROM_DISPNAME eggs')
        t = self.obj.FromDisplayName
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testFromHandle(self):
        # Readable, Type: str
        self.api.enqueue('GET CHATMESSAGE 1234 FROM_HANDLE',
                         'CHATMESSAGE 1234 FROM_HANDLE eggs')
        t = self.obj.FromHandle
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testId(self):
        # Readable, Type: int
        t = self.obj.Id
        self.assertInstance(t, int)
        self.assertEqual(t, 1234)
        self.failUnless(self.api.is_empty())

    def testIsEditable(self):
        # Readable, Type: bool
        self.api.enqueue('GET CHATMESSAGE 1234 IS_EDITABLE',
                         'CHATMESSAGE 1234 IS_EDITABLE TRUE')
        t = self.obj.IsEditable
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())

    def testLeaveReason(self):
        # Readable, Type: str
        self.api.enqueue('GET CHATMESSAGE 1234 LEAVEREASON',
                         'CHATMESSAGE 1234 LEAVEREASON USER_NOT_FOUND')
        t = self.obj.LeaveReason
        self.assertInstance(t, str)
        self.assertEqual(t, 'USER_NOT_FOUND')
        self.failUnless(self.api.is_empty())

    def testSeen(self):
        # Writable, Type: bool
        from warnings import simplefilter
        self.api.enqueue('SET CHATMESSAGE 1234 SEEN',
                         'CHATMESSAGE 1234 STATUS READ')
        try:
            simplefilter('ignore')
            self.obj.Seen = True
        finally:
            simplefilter('default')
        self.failUnless(self.api.is_empty())

    def testSender(self):
        # Readable, Type: User
        self.api.enqueue('GET CHATMESSAGE 1234 FROM_HANDLE',
                         'CHATMESSAGE 1234 FROM_HANDLE eggs')
        t = self.obj.Sender
        self.assertInstance(t, User)
        self.assertEqual(t.Handle, 'eggs')
        self.failUnless(self.api.is_empty())

    def testStatus(self):
        # Readable, Type: str
        self.api.enqueue('GET CHATMESSAGE 1234 STATUS',
                         'CHATMESSAGE 1234 STATUS SENDING')
        t = self.obj.Status
        self.assertInstance(t, str)
        self.assertEqual(t, 'SENDING')
        self.failUnless(self.api.is_empty())

    def testTimestamp(self):
        # Readable, Type: float
        self.api.enqueue('GET CHATMESSAGE 1234 TIMESTAMP',
                         'CHATMESSAGE 1234 TIMESTAMP 123.4')
        t = self.obj.Timestamp
        self.assertInstance(t, float)
        self.assertEqual(t, 123.4)
        self.failUnless(self.api.is_empty())

    def testType(self):
        # Readable, Type: str
        self.api.enqueue('GET CHATMESSAGE 1234 TYPE',
                         'CHATMESSAGE 1234 TYPE TEXT')
        t = self.obj.Type
        self.assertInstance(t, str)
        self.assertEqual(t, 'TEXT')
        self.failUnless(self.api.is_empty())

    def testUsers(self):
        # Readable, Type: UserCollection
        self.api.enqueue('GET CHATMESSAGE 1234 USERS',
                         'CHATMESSAGE 1234 USERS eggs sausage')
        t = self.obj.Users
        self.assertInstance(t, UserCollection)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())


class ChatMemberTest(skype4pytest.TestCase):
    def setUpObject(self):
        self.obj = ChatMember(self.skype, '1234')

    # Methods
    # =======

    def testCanSetRoleTo(self):
        # Returned type: bool
        self.api.enqueue('ALTER CHATMEMBER 1234 CANSETROLETO HELPER',
                         'ALTER CHATMEMBER CANSETROLETO TRUE')
        t = self.obj.CanSetRoleTo('HELPER')
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())

    # Properties
    # ==========

    def testChat(self):
        # Readable, Type: Chat
        self.api.enqueue('GET CHATMEMBER 1234 CHATNAME',
                         'CHATMEMBER 1234 CHATNAME eggs')
        t = self.obj.Chat
        self.assertInstance(t, Chat)
        self.assertEqual(t.Name, 'eggs')
        self.failUnless(self.api.is_empty())

    def testHandle(self):
        # Readable, Type: str
        self.api.enqueue('GET CHATMEMBER 1234 IDENTITY',
                         'CHATMEMBER 1234 IDENTITY eggs')
        t = self.obj.Handle
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testId(self):
        # Readable, Type: int
        t = self.obj.Id
        self.assertInstance(t, int)
        self.assertEqual(t, 1234)
        self.failUnless(self.api.is_empty())

    def testIsActive(self):
        # Readable, Type: bool
        self.api.enqueue('GET CHATMEMBER 1234 IS_ACTIVE',
                         'CHATMEMBER 1234 IS_ACTIVE TRUE')
        t = self.obj.IsActive
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())

    def testRole(self):
        # Readable, Writable, Type: str
        self.api.enqueue('GET CHATMEMBER 1234 ROLE',
                         'CHATMEMBER 1234 ROLE HELPER')
        t = self.obj.Role
        self.assertInstance(t, str)
        self.assertEqual(t, 'HELPER')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('ALTER CHATMEMBER 1234 SETROLETO HELPER')
        self.obj.Role = 'HELPER'
        self.failUnless(self.api.is_empty())


def suite():
    return unittest.TestSuite([
        unittest.defaultTestLoader.loadTestsFromTestCase(ChatTest),
        unittest.defaultTestLoader.loadTestsFromTestCase(ChatMessageTest),
        unittest.defaultTestLoader.loadTestsFromTestCase(ChatMemberTest),
    ])


if __name__ == '__main__':
    unittest.main()
