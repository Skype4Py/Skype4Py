import unittest

import skype4pytest
from Skype4Py.skype import *


class SkypeTest(skype4pytest.TestCase):
    def setUpObject(self):
        self.obj = self.skype

    # Methods
    # =======

    def testApiSecurityContextEnabled(self):
        # Returned type: bool
        def test():
            self.obj.ApiSecurityContextEnabled('spam')
        self.failUnlessRaises(SkypeAPIError, test)

    def testApplication(self):
        # Returned type: Application
        t = self.obj.Application('spam')
        self.assertInstance(t, Application)

    def testAsyncSearchUsers(self):
        # Returned type: int
        self.api.enqueue('SEARCH USERS spam',
                         'USERS eggs, sausage, bacon')
        t = self.obj.AsyncSearchUsers('spam')
        self.assertInstance(t, int)
        self.assertEqual(t, 0)
        self.failUnless(self.api.is_empty())

    def testAttach(self):
        self.api.set_attachment_status(apiAttachUnknown)
        self.obj.Attach()
        self.assertEqual(self.obj.AttachmentStatus, apiAttachSuccess)

    def testCall(self):
        # Returned type: Call
        self.api.enqueue('GET CALL 345 STATUS',
                         'CALL 345 STATUS spam')
        t = self.obj.Call(345)
        self.assertInstance(t, Call)
        self.assertEqual(t.Id, 345)
        self.assertEqual(t.Status, 'spam')
        self.failUnless(self.api.is_empty())

    def testCalls(self):
        # Returned type: CallCollection
        self.api.enqueue('SEARCH CALLS spam',
                         'CALLS 123, 456, 789')
        t = self.obj.Calls('spam')
        self.assertInstance(t, CallCollection)
        self.assertEqual(len(t), 3)
        self.assertEqual(t[1].Id, 456)
        self.failUnless(self.api.is_empty())

    def testChangeUserStatus(self):
        self.api.enqueue('GET USERSTATUS',
                         'USERSTATUS spam')
        self.api.enqueue('SET USERSTATUS eggs',
                         'USERSTATUS eggs')
        self.obj.ChangeUserStatus('eggs')
        self.assertEqual(self.obj.CurrentUserStatus, 'eggs')
        self.failUnless(self.api.is_empty())

    def testChat(self):
        # Returned type: chat.Chat
        self.api.enqueue('GET CHAT spam STATUS',
                         'CHAT spam STATUS eggs')
        t = self.obj.Chat('spam')
        self.assertInstance(t, Chat)
        self.assertEqual(t.Name, 'spam')
        self.assertEqual(t.Status, 'eggs')
        self.failUnless(self.api.is_empty())

    def testClearCallHistory(self):
        self.api.enqueue('CLEAR CALLHISTORY ALL spam')
        self.obj.ClearCallHistory('spam')
        self.failUnless(self.api.is_empty())

    def testClearChatHistory(self):
        self.api.enqueue('CLEAR CHATHISTORY')
        self.obj.ClearChatHistory()
        self.failUnless(self.api.is_empty())

    def testClearVoicemailHistory(self):
        self.api.enqueue('CLEAR VOICEMAILHISTORY')
        self.obj.ClearVoicemailHistory()
        self.failUnless(self.api.is_empty())

    def testCommand(self):
        # Returned type: Command
        t = self.obj.Command('SPAM')
        self.assertInstance(t, Command)
        self.assertEqual(t.Command, 'SPAM')

    def testConference(self):
        # Returned type: Conference
        self.api.enqueue('SEARCH CALLS ',
                         'CALLS 123, 456')
        self.api.enqueue('GET CALL 123 CONF_ID',
                         'CALL 123 CONF_ID 789')
        self.api.enqueue('GET CALL 456 CONF_ID',
                         'CALL 456 CONF_ID 789')
        t = self.obj.Conference(789)
        self.assertInstance(t, Conference)
        self.assertEqual(t.Id, 789)
        self.failUnless(self.api.is_empty())

    def testCreateChatUsingBlob(self):
        # Returned type: chat.Chat
        self.api.enqueue('CHAT CREATEUSINGBLOB spam',
                         'CHAT eggs NAME eggs')
        t = self.obj.CreateChatUsingBlob('spam')
        self.assertInstance(t, Chat)
        self.assertEqual(t.Name, 'eggs')
        self.failUnless(self.api.is_empty())

    def testCreateChatWith(self):
        # Returned type: Chat
        self.api.enqueue('CHAT CREATE spam, eggs',
                         'CHAT sausage STATUS bacon')
        t = self.obj.CreateChatWith('spam', 'eggs')
        self.assertInstance(t, Chat)
        self.failUnless(self.api.is_empty())

    def testCreateGroup(self):
        # Returned type: Group
        self.api.enqueue('SEARCH GROUPS CUSTOM',
                         'GROUPS 123, 789')
        self.api.enqueue('CREATE GROUP spam')
        self.api.enqueue('SEARCH GROUPS CUSTOM',
                         'GROUPS 123, 456, 789')
        self.api.enqueue('GET GROUP 456 DISPLAYNAME',
                         'GROUP 456 DISPLAYNAME spam')
        t = self.obj.CreateGroup('spam')
        self.assertInstance(t, Group)
        self.assertEqual(t.Id, 456)
        self.assertEqual(t.DisplayName, 'spam')
        self.failUnless(self.api.is_empty())

    def testCreateSms(self):
        # Returned type: SmsMessage
        self.api.enqueue('CREATE SMS OUTGOING +1234567890',
                         'SMS 123 TYPE OUTGOING')
        t = self.obj.CreateSms(smsMessageTypeOutgoing, '+1234567890')
        self.assertInstance(t, SmsMessage)
        self.assertEqual(t.Id, 123)
        self.failUnless(self.api.is_empty())

    def testDeleteGroup(self):
        self.api.enqueue('DELETE GROUP 789')
        self.obj.DeleteGroup(789)
        self.failUnless(self.api.is_empty())

    def testEnableApiSecurityContext(self):
        def test():
            self.obj.EnableApiSecurityContext('spam')
        self.failUnlessRaises(SkypeAPIError, test)

    def testFindChatUsingBlob(self):
        # Returned type: chat.Chat
        self.api.enqueue('CHAT FINDUSINGBLOB spam',
                         'CHAT eggs STATUS MULTI_SUBSCRIBED')
        t = self.obj.FindChatUsingBlob('spam')
        self.assertInstance(t, Chat)
        self.assertEqual(t.Name, 'eggs')
        self.failUnless(self.api.is_empty())

    def testGreeting(self):
        # Returned type: Voicemail
        self.api.enqueue('SEARCH VOICEMAILS',
                         'VOICEMAILS 123, 456')
        self.api.enqueue('GET VOICEMAIL 123 PARTNER_HANDLE',
                         'VOICEMAIL 123 PARTNER_HANDLE spam')
        self.api.enqueue('GET VOICEMAIL 123 TYPE',
                         'VOICEMAIL 123 TYPE DEFAULT_GREETING')
        t = self.obj.Greeting('spam')
        self.assertInstance(t, Voicemail)
        self.assertEqual(t.Id, 123)
        self.failUnless(self.api.is_empty())

    def testMessage(self):
        # Returned type: ChatMessage
        self.api.enqueue('GET CHATMESSAGE 123 STATUS',
                         'CHATMESSAGE 123 STATUS RECEIVED')
        t = self.obj.Message(123)
        self.assertInstance(t, ChatMessage)
        self.assertEqual(t.Id, 123)
        self.assertEqual(t.Status, cmsReceived)
        self.failUnless(self.api.is_empty())

    def testMessages(self):
        # Returned type: ChatMessageCollection
        self.api.enqueue('SEARCH CHATMESSAGES spam',
                         'CHATMESSAGES 123, 456')
        t = self.obj.Messages('spam')
        self.assertInstance(t, ChatMessageCollection)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())

    def testPlaceCall(self):
        # Returned type: Call
        self.api.enqueue('SEARCH ACTIVECALLS',
                         'ACTIVECALLS ')
        self.api.enqueue('CALL spam',
                         'CALL 123 STATUS UNPLACED')
        t = self.obj.PlaceCall('spam')
        self.assertInstance(t, Call)
        self.assertEqual(t.Id, 123)
        self.failUnless(self.api.is_empty())

    def testPrivilege(self):
        # Returned type: bool
        self.api.enqueue('GET PRIVILEGE SPAM',
                         'PRIVILEGE SPAM TRUE')
        t = self.obj.Privilege('spam')
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())

    def testProfile(self):
        # Returned type: unicode or None
        self.api.enqueue('GET PROFILE FULLNAME',
                         'PROFILE FULLNAME spam eggs')
        t = self.obj.Profile('FULLNAME')
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'spam eggs')
        self.failUnless(self.api.is_empty())

    def testProperty(self):
        # Returned type: unicode or None
        self.api.enqueue('GET CHAT spam STATUS',
                         'CHAT spam STATUS DIALOG')
        t = self.obj.Property('CHAT', 'spam', 'STATUS')
        self.assertInstance(t, unicode)
        self.assertEqual(t, chsDialog)
        self.failUnless(self.api.is_empty())

    def testRegisterEventHandler(self):
        # Returned type: bool
        from threading import Event
        event = Event()
        def handler(user, mood_text):
            self.assertEqual(user.Handle, 'spam')
            self.assertEqual(mood_text, 'eggs')
            event.set()
        t = self.obj.RegisterEventHandler('UserMood', handler)
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.api.schedule(0, 'USER spam MOOD_TEXT eggs')
        event.wait(1)
        self.assertEqual(event.isSet(), True)
        t = self.obj.UnregisterEventHandler('UserMood', handler)
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        t = self.obj.UnregisterEventHandler('UserMood', handler)
        self.assertEqual(t, False)

    def testResetCache(self):
        self.obj._CacheDict['SPAM'] = 'EGGS'
        self.obj.ResetCache()
        self.assertEqual(len(self.obj._CacheDict), 0)

    def testSearchForUsers(self):
        # Returned type: UserCollection
        self.api.enqueue('SEARCH USERS spam',
                         'USERS eggs, sausage')
        t = self.obj.SearchForUsers('spam')
        self.assertInstance(t, UserCollection)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())

    def testSendCommand(self):
        self.api.enqueue('SPAM',
                         'EGGS')
        command = self.obj.Command('SPAM')
        self.obj.SendCommand(command)
        self.assertEqual(command.Reply, 'EGGS')
        self.failUnless(self.api.is_empty())

    def testSendMessage(self):
        # Returned type: ChatMessage
        self.api.enqueue('CHAT CREATE spam',
                         'CHAT eggs STATUS DIALOG')
        self.api.enqueue('CHATMESSAGE eggs sausage',
                         'CHATMESSAGE 123 STATUS SENDING')
        t = self.obj.SendMessage('spam', 'sausage')
        self.assertInstance(t, ChatMessage)
        self.assertEqual(t.Id, 123)
        self.failUnless(self.api.is_empty())

    def testSendSms(self):
        # Returned type: SmsMessage
        self.api.enqueue('CREATE SMS OUTGOING spam',
                         'SMS 123 TYPE OUTGOING')
        self.api.enqueue('SET SMS 123 BODY eggs',
                         'SMS 123 BODY eggs')
        self.api.enqueue('ALTER SMS 123 SEND')
        t = self.obj.SendSms('spam', Body='eggs')
        self.assertInstance(t, SmsMessage)
        self.assertEqual(t.Id, 123)
        self.failUnless(self.api.is_empty())

    def testSendVoicemail(self):
        # Returned type: Voicemail
        self.api.enqueue('CALLVOICEMAIL spam',
                         'CALL 123 STATUS ROUTING')
        self.api.protocol = 6
        t = self.obj.SendVoicemail('spam')
        # TODO: As of now the method does not yet return the Voicemail object.
        #self.assertInstance(t, Voicemail)
        #self.assertEqual(t.Id, 345)
        self.failUnless(self.api.is_empty())

    def testUser(self):
        # Returned type: User
        self.api.enqueue('GET CURRENTUSERHANDLE',
                         'CURRENTUSERHANDLE spam')
        self.api.enqueue('GET USER spam ONLINESTATUS',
                         'USER spam ONLINESTATUS OFFLINE')
        t = self.obj.User()
        self.assertInstance(t, User)
        self.assertEqual(t.Handle, 'spam')
        self.assertEqual(t.OnlineStatus, olsOffline)
        self.failUnless(self.api.is_empty())

    def testVariable(self):
        # Returned type: unicode or None
        self.api.enqueue('GET SPAM',
                         'SPAM eggs')
        t = self.obj.Variable('SPAM')
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())

    def testVoicemail(self):
        # Returned type: Voicemail
        self.api.enqueue('GET VOICEMAIL 345 TYPE',
                         'VOICEMAIL 345 TYPE OUTGOING')
        t = self.obj.Voicemail(345)
        self.assertInstance(t, Voicemail)
        self.assertEqual(t.Id, 345)
        self.assertEqual(t.Type, vmtOutgoing)
        self.failUnless(self.api.is_empty())

    # Properties
    # ==========

    def testActiveCalls(self):
        # Readable, Type: CallCollection
        self.api.enqueue('SEARCH ACTIVECALLS',
                         'ACTIVECALLS 123, 456')
        t = self.obj.ActiveCalls
        self.assertInstance(t, CallCollection)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())

    def testActiveChats(self):
        # Readable, Type: ChatCollection
        self.api.enqueue('SEARCH ACTIVECHATS',
                         'ACTIVECHATS spam, eggs, sausage, ham')
        t = self.obj.ActiveChats
        self.assertInstance(t, ChatCollection)
        self.assertEqual(len(t), 4)
        self.failUnless(self.api.is_empty())

    def _testActiveFileTransfers(self):
        # Readable, Type: FileTransferCollection
        self.api.enqueue('SEARCH ACTIVEFILETRANSFERS',
                         'ACTIVEFILETRANSFERS 123, 456, 789')
        t = self.obj.ActiveFileTransfers
        self.assertInstance(t, FileTransferCollection)
        self.assertEqual(len(t), 3)
        self.failUnless(self.api.is_empty())

    def testApiWrapperVersion(self):
        # Readable, Type: str
        t = self.obj.ApiWrapperVersion
        self.assertInstance(t, str)
        from Skype4Py import __version__
        self.assertEqual(t, __version__)

    def testAttachmentStatus(self):
        # Readable, Type: int
        t = self.obj.AttachmentStatus
        self.assertInstance(t, int)
        # API emulator is always attached.
        self.assertEqual(t, apiAttachSuccess)

    def testBookmarkedChats(self):
        # Readable, Type: ChatCollection
        self.api.enqueue('SEARCH BOOKMARKEDCHATS',
                         'BOOKMARKEDCHATS spam, eggs, ham')
        t = self.obj.BookmarkedChats
        self.assertInstance(t, ChatCollection)
        self.assertEqual(len(t), 3)
        self.failUnless(self.api.is_empty())

    def testCache(self):
        # Readable, Writable, Type: bool
        t = self.obj.Cache
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.obj.Cache = False
        t = self.obj.Cache
        self.assertEqual(t, False)

    def testChats(self):
        # Readable, Type: ChatCollection
        self.api.enqueue('SEARCH CHATS',
                         'CHATS spam, eggs')
        t = self.obj.Chats
        self.assertInstance(t, ChatCollection)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())

    def testClient(self):
        # Readable, Type: Client
        t = self.obj.Client
        self.assertInstance(t, Client)

    def testCommandId(self):
        # Readable, Writable, Type: bool
        t = self.obj.CommandId
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        def test():
            self.obj.CommandId = False
        self.failUnlessRaises(SkypeError, test)

    def testConferences(self):
        # Readable, Type: ConferenceCollection
        self.api.enqueue('SEARCH CALLS ',
                         'CALLS 123, 456')
        self.api.enqueue('GET CALL 123 CONF_ID',
                         'CALL 123 CONF_ID 789')
        self.api.enqueue('GET CALL 456 CONF_ID',
                         'CALL 456 CONF_ID 789')
        t = self.obj.Conferences
        self.assertInstance(t, ConferenceCollection)
        self.assertEqual(len(t), 1)
        self.assertEqual(t[0].Id, 789)
        self.failUnless(self.api.is_empty())

    def testConnectionStatus(self):
        # Readable, Type: str
        self.api.enqueue('GET CONNSTATUS',
                         'CONNSTATUS CONNECTING')
        t = self.obj.ConnectionStatus
        self.assertInstance(t, str)
        self.assertEqual(t, conConnecting)
        self.failUnless(self.api.is_empty())

    def testConvert(self):
        # Readable, Type: Conversion
        t = self.obj.Convert
        self.assertInstance(t, Conversion)

    def testCurrentUser(self):
        # Readable, Type: User
        self.api.enqueue('GET CURRENTUSERHANDLE',
                         'CURRENTUSERHANDLE spam')
        t = self.obj.CurrentUser
        self.assertInstance(t, User)
        self.assertEqual(t.Handle, 'spam')
        self.failUnless(self.api.is_empty())

    def testCurrentUserHandle(self):
        # Readable, Type: str
        self.api.enqueue('GET CURRENTUSERHANDLE',
                         'CURRENTUSERHANDLE spam')
        t = self.obj.CurrentUserHandle
        self.assertInstance(t, str)
        self.assertEqual(t, 'spam')
        self.failUnless(self.api.is_empty())

    def testCurrentUserProfile(self):
        # Readable, Type: Profile
        t = self.obj.CurrentUserProfile
        self.assertInstance(t, Profile)

    def testCurrentUserStatus(self):
        # Readable, Writable, Type: str
        self.api.enqueue('GET USERSTATUS',
                         'USERSTATUS NA')
        t = self.obj.CurrentUserStatus
        self.assertInstance(t, str)
        self.assertEqual(t, cusNotAvailable)
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET USERSTATUS AWAY',
                         'USERSTATUS AWAY')
        self.obj.CurrentUserStatus = cusAway
        self.failUnless(self.api.is_empty())

    def testCustomGroups(self):
        # Readable, Type: GroupCollection
        self.api.enqueue('SEARCH GROUPS CUSTOM',
                         'GROUPS 123, 456, 789')
        t = self.obj.CustomGroups
        self.assertInstance(t, GroupCollection)
        self.assertEqual(len(t), 3)
        self.failUnless(self.api.is_empty())

    def testFileTransfers(self):
        # Readable, Type: FileTransferCollection
        self.api.enqueue('SEARCH FILETRANSFERS',
                         'FILETRANSFERS 123, 456')
        t = self.obj.FileTransfers
        self.assertInstance(t, FileTransferCollection)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())

    def testFocusedContacts(self):
        # Readable, Type: UserCollection
        self.api.enqueue('GET CONTACTS_FOCUSED',
                         'CONTACTS FOCUSED spam, eggs')
        t = self.obj.FocusedContacts
        self.assertInstance(t, UserCollection)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())

    def testFriendlyName(self):
        # Readable, Writable, Type: unicode
        self.obj.FriendlyName = 'spam'
        t = self.obj.FriendlyName
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'spam')

    def testFriends(self):
        # Readable, Type: UserCollection
        self.api.enqueue('SEARCH FRIENDS',
                         'FRIENDS spam, eggs, sausage')
        t = self.obj.Friends
        self.assertInstance(t, UserCollection)
        self.assertEqual(len(t), 3)
        self.failUnless(self.api.is_empty())

    def testGroups(self):
        # Readable, Type: GroupCollection
        self.api.enqueue('SEARCH GROUPS ALL',
                         'GROUPS 123, 456')
        t = self.obj.Groups
        self.assertInstance(t, GroupCollection)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())

    def testHardwiredGroups(self):
        # Readable, Type: GroupCollection
        self.api.enqueue('SEARCH GROUPS HARDWIRED',
                         'GROUPS 123, 456, 789')
        t = self.obj.HardwiredGroups
        self.assertInstance(t, GroupCollection)
        self.assertEqual(len(t), 3)
        self.failUnless(self.api.is_empty())

    def testMissedCalls(self):
        # Readable, Type: CallCollection
        self.api.enqueue('SEARCH MISSEDCALLS',
                         'MISSEDCALLS 123, 456')
        t = self.obj.MissedCalls
        self.assertInstance(t, CallCollection)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())

    def testMissedChats(self):
        # Readable, Type: ChatCollection
        self.api.enqueue('SEARCH MISSEDCHATS',
                         'MISSEDCHATS spam, eggs, ham')
        t = self.obj.MissedChats
        self.assertInstance(t, ChatCollection)
        self.assertEqual(len(t), 3)
        self.failUnless(self.api.is_empty())

    def testMissedMessages(self):
        # Readable, Type: ChatMessageCollection
        self.api.enqueue('SEARCH MISSEDCHATMESSAGES',
                         'MISSEDCHATMESSAGES 123, 456, 789')
        t = self.obj.MissedMessages
        self.assertInstance(t, ChatMessageCollection)
        self.assertEqual(len(t), 3)
        self.failUnless(self.api.is_empty())

    def testMissedSmss(self):
        # Readable, Type: SmsMessageCollection
        self.api.enqueue('SEARCH MISSEDSMSS',
                         'MISSEDSMSS 123, 456')
        t = self.obj.MissedSmss
        self.assertInstance(t, SmsMessageCollection)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())

    def testMissedVoicemails(self):
        # Readable, Type: VoicemailCollection
        self.api.enqueue('SEARCH MISSEDVOICEMAILS',
                         'MISSEDVOICEMAILS 123, 456, 7, 8, 9')
        t = self.obj.MissedVoicemails
        self.assertInstance(t, VoicemailCollection)
        self.assertEqual(len(t), 5)
        self.failUnless(self.api.is_empty())

    def testMute(self):
        # Readable, Writable, Type: bool
        self.api.enqueue('GET MUTE',
                         'MUTE ON')
        t = self.obj.Mute
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET MUTE OFF',
                         'MUTE OFF')
        self.obj.Mute = False
        self.failUnless(self.api.is_empty())

    def testPredictiveDialerCountry(self):
        # Readable, Type: str
        self.api.enqueue('GET PREDICTIVE_DIALER_COUNTRY',
                         'PREDICTIVE_DIALER_COUNTRY de')
        t = self.obj.PredictiveDialerCountry
        self.assertInstance(t, str)
        self.assertEqual(t, 'de')
        self.failUnless(self.api.is_empty())

    def testProtocol(self):
        # Readable, Writable, Type: int
        t = self.obj.Protocol
        self.assertInstance(t, int)
        from Skype4Py.api import DEFAULT_PROTOCOL
        self.assertEqual(t, DEFAULT_PROTOCOL)
        self.api.enqueue('PROTOCOL 10')
        self.obj.Protocol = 10
        t = self.obj.Protocol
        self.assertEqual(t, 10)
        self.failUnless(self.api.is_empty())

    def testRecentChats(self):
        # Readable, Type: ChatCollection
        self.api.enqueue('SEARCH RECENTCHATS',
                         'RECENTCHATS spam, eggs')
        t = self.obj.RecentChats
        self.assertInstance(t, ChatCollection)
        self.assertEqual(len(t), 2)
        self.failUnless(self.api.is_empty())

    def testSettings(self):
        # Readable, Type: Settings
        t = self.obj.Settings
        self.assertInstance(t, Settings)

    def testSilentMode(self):
        # Readable, Writable, Type: bool
        self.api.enqueue('GET SILENT_MODE',
                         'SILENT_MODE ON')
        t = self.obj.SilentMode
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET SILENT_MODE OFF',
                         'SILENT_MODE OFF')
        self.obj.SilentMode = False
        self.failUnless(self.api.is_empty())

    def testSmss(self):
        # Readable, Type: SmsMessageCollection
        self.api.enqueue('SEARCH SMSS',
                         'SMSS 123, 456, 789')
        t = self.obj.Smss
        self.assertInstance(t, SmsMessageCollection)
        self.assertEqual(len(t), 3)
        self.failUnless(self.api.is_empty())

    def testTimeout(self):
        # Readable, Writable, Type: float, int or long
        t = self.obj.Timeout
        self.assertInstance(t, int)
        from Skype4Py.api import DEFAULT_TIMEOUT
        self.assertEqual(t, DEFAULT_TIMEOUT)
        self.obj.Timeout = 23.4
        t = self.obj.Timeout
        self.assertEqual(t, 23.4)

    def testUsersWaitingAuthorization(self):
        # Readable, Type: UserCollection
        self.api.enqueue('SEARCH USERSWAITINGMYAUTHORIZATION',
                         'USERSWAITINGMYAUTHORIZATION spam, eggs, ham')
        t = self.obj.UsersWaitingAuthorization
        self.assertInstance(t, UserCollection)
        self.assertEqual(len(t), 3)
        self.failUnless(self.api.is_empty())

    def testVersion(self):
        # Readable, Type: str
        self.api.enqueue('GET SKYPEVERSION',
                         'SKYPEVERSION spam.eggs')
        t = self.obj.Version
        self.assertInstance(t, str)
        self.assertEqual(t, 'spam.eggs')
        self.failUnless(self.api.is_empty())

    def testVoicemails(self):
        # Readable, Type: VoicemailCollection
        self.api.enqueue('SEARCH VOICEMAILS',
                         'VOICEMAILS 123, 456, 789')
        t = self.obj.Voicemails
        self.assertInstance(t, VoicemailCollection)
        self.assertEqual(len(t), 3)
        self.failUnless(self.api.is_empty())


def suite():
    return unittest.TestSuite([
        unittest.defaultTestLoader.loadTestsFromTestCase(SkypeTest),
    ])


if __name__ == '__main__':
    unittest.main()
