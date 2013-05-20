"""Chats.
"""
__docformat__ = 'restructuredtext en'


from utils import *
from user import *
from errors import SkypeError


class Chat(Cached):
    """Represents a Skype chat.
    """
    _ValidateHandle = str

    def __repr__(self):
        return Cached.__repr__(self, 'Name')

    def _Alter(self, AlterName, Args=None):
        '''
        --- Prajna bug fix ---
        Original code:
        return self._Owner._Alter('CHAT', self.Name, AlterName, Args,
                                  'ALTER CHAT %s %s' % (self.Name, AlterName))
        Whereas most of the ALTER commands echo the command in the reply,
        the ALTER CHAT commands strip the <chat_id> from the reply,
        so we need to do the same for the expected reply
        '''
        return self._Owner._Alter('CHAT', self.Name, AlterName, Args,
                                  'ALTER CHAT %s' % (AlterName))

    def _Property(self, PropName, Value=None, Cache=True):
        return self._Owner._Property('CHAT', self.Name, PropName, Value, Cache)

    def AcceptAdd(self):
        """Accepts a shared group add request.
        """
        self._Alter('ACCEPTADD')

    def AddMembers(self, *Members):
        """Adds new members to the chat.

        :Parameters:
          Members : `User`
            One or more users to add.
        """
        self._Alter('ADDMEMBERS', ', '.join([x.Handle for x in Members]))

    def Bookmark(self):
        """Bookmarks the chat in Skype client.
        """
        self._Alter('BOOKMARK')

    def ClearRecentMessages(self):
        """Clears recent chat messages.
        """
        self._Alter('CLEARRECENTMESSAGES')

    def Disband(self):
        """Ends the chat.
        """
        self._Alter('DISBAND')

    def EnterPassword(self, Password):
        """Enters chat password.

        :Parameters:
          Password : unicode
            Password
        """
        self._Alter('ENTERPASSWORD', tounicode(Password))

    def Join(self):
        """Joins the chat.
        """
        self._Alter('JOIN')

    def Kick(self, *Handles):
        """Kicks member(s) from chat.

        :Parameters:
          Handles : str
            Skype username(s).
        """
        self._Alter('KICK', ', '.join(Handles))

    def KickBan(self, *Handles):
        """Kicks and bans member(s) from chat.

        :Parameters:
          Handles : str
            Skype username(s).
        """
        self._Alter('KICKBAN', ', '.join(Handles))

    def Leave(self):
        """Leaves the chat.
        """
        self._Alter('LEAVE')

    def OpenWindow(self):
        """Opens the chat window.
        """
        self._Owner.Client.OpenDialog('CHAT', self.Name)

    def SendMessage(self, MessageText):
        """Sends a chat message.

        :Parameters:
          MessageText : unicode
            Message text

        :return: Message object
        :rtype: `ChatMessage`
        """
        return ChatMessage(self._Owner, chop(self._Owner._DoCommand('CHATMESSAGE %s %s' % (self.Name,
            tounicode(MessageText))), 2)[1])

    def SetPassword(self, Password, Hint=''):
        """Sets the chat password.

        :Parameters:
          Password : unicode
            Password
          Hint : unicode
            Password hint
        """
        if ' ' in Password:
            raise ValueError('Password mut be one word')
        self._Alter('SETPASSWORD', '%s %s' % (tounicode(Password), tounicode(Hint)))

    def Unbookmark(self):
        """Unbookmarks the chat.
        """
        self._Alter('UNBOOKMARK')

    def _GetActiveMembers(self):
        return UserCollection(self._Owner, split(self._Property('ACTIVEMEMBERS', Cache=False)))

    ActiveMembers = property(_GetActiveMembers,
    doc="""Active members of a chat.

    :type: `UserCollection`
    """)

    def _GetActivityDatetime(self):
        from datetime import datetime
        return datetime.fromtimestamp(self.ActivityTimestamp)

    ActivityDatetime = property(_GetActivityDatetime,
    doc="""Returns chat activity timestamp as datetime.

    :type: datetime.datetime
    """)

    def _GetActivityTimestamp(self):
        return float(self._Property('ACTIVITY_TIMESTAMP'))

    ActivityTimestamp = property(_GetActivityTimestamp,
    doc="""Returns chat activity timestamp.

    :type: float

    :see: `ActivityDatetime`
    """)

    def _GetAdder(self):
        return User(self._Owner, self._Property('ADDER'))

    Adder = property(_GetAdder,
    doc="""Returns the user that added current user to the chat.

    :type: `User`
    """)

    def _SetAlertString(self, Value):
        self._Alter('SETALERTSTRING', quote('=%s' % tounicode(Value)))

    AlertString = property(fset=_SetAlertString,
    doc="""Chat alert string. Only messages containing words from this string will cause a
    notification to pop up on the screen.

    :type: unicode
    """)

    def _GetApplicants(self):
        return UserCollection(self._Owner, split(self._Property('APPLICANTS')))

    Applicants = property(_GetApplicants,
    doc="""Chat applicants.

    :type: `UserCollection`
    """)

    def _GetBlob(self):
        return str(self._Property('BLOB'))

    Blob = property(_GetBlob,
    doc="""Chat blob.

    :type: str
    """)

    def _GetBookmarked(self):
        return (self._Property('BOOKMARKED') == 'TRUE')

    Bookmarked = property(_GetBookmarked,
    doc="""Tells if this chat is bookmarked.

    :type: bool
    """)

    def _GetDatetime(self):
        from datetime import datetime
        return datetime.fromtimestamp(self.Timestamp)

    Datetime = property(_GetDatetime,
    doc="""Chat timestamp as datetime.

    :type: datetime.datetime
    """)

    def _GetDescription(self):
        return self._Property('DESCRIPTION')

    def _SetDescription(self, Value):
        self._Property('DESCRIPTION', tounicode(Value))

    Description = property(_GetDescription, _SetDescription,
    doc="""Chat description.

    :type: unicode
    """)

    def _GetDialogPartner(self):
        return str(self._Property('DIALOG_PARTNER'))

    DialogPartner = property(_GetDialogPartner,
    doc="""Skypename of the chat dialog partner.

    :type: str
    """)

    def _GetFriendlyName(self):
        return self._Property('FRIENDLYNAME')

    FriendlyName = property(_GetFriendlyName,
    doc="""Friendly name of the chat.

    :type: unicode
    """)

    def _GetGuideLines(self):
        return self._Property('GUIDELINES')

    def _SetGuideLines(self, Value):
        self._Alter('SETGUIDELINES', tounicode(Value))

    GuideLines = property(_GetGuideLines, _SetGuideLines,
    doc="""Chat guidelines.

    :type: unicode
    """)

    def _GetMemberObjects(self):
        return ChatMemberCollection(self._Owner, split(self._Property('MEMBEROBJECTS'), ', '))

    MemberObjects = property(_GetMemberObjects,
    doc="""Chat members as member objects.

    :type: `ChatMemberCollection`
    """)

    def _GetMembers(self):
        return UserCollection(self._Owner, split(self._Property('MEMBERS')))

    Members = property(_GetMembers,
    doc="""Chat members.

    :type: `UserCollection`
    """)

    def _GetMessages(self):
        return ChatMessageCollection(self._Owner, split(self._Property('CHATMESSAGES', Cache=False), ', '))

    Messages = property(_GetMessages,
    doc="""All chat messages.

    :type: `ChatMessageCollection`
    """)

    def _GetMyRole(self):
        return str(self._Property('MYROLE'))

    MyRole = property(_GetMyRole,
    doc="""My chat role in a public chat.

    :type: `enums`.chatMemberRole*
    """)

    def _GetMyStatus(self):
        return str(self._Property('MYSTATUS'))

    MyStatus = property(_GetMyStatus,
    doc="""My status in a public chat.

    :type: `enums`.chatStatus*
    """)

    def _GetName(self):
        return self._Handle

    Name = property(_GetName,
    doc="""Chat name as used by Skype to identify this chat.

    :type: str
    """)

    def _GetOptions(self):
        return int(self._Property('OPTIONS'))

    def _SetOptions(self, Value):
        self._Alter('SETOPTIONS', Value)

    Options = property(_GetOptions, _SetOptions,
    doc="""Chat options. A mask.

    :type: `enums`.chatOption*
    """)

    def _GetPasswordHint(self):
        return self._Property('PASSWORDHINT')

    PasswordHint = property(_GetPasswordHint,
    doc="""Chat password hint.

    :type: unicode
    """)

    def _GetPosters(self):
        return UserCollection(self._Owner, split(self._Property('POSTERS')))

    Posters = property(_GetPosters,
    doc="""Users who have posted messages to this chat.

    :type: `UserCollection`
    """)

    def _GetRecentMessages(self):
        return ChatMessageCollection(self._Owner, split(self._Property('RECENTCHATMESSAGES', Cache=False), ', '))

    RecentMessages = property(_GetRecentMessages,
    doc="""Most recent chat messages.

    :type: `ChatMessageCollection`
    """)

    def _GetStatus(self):
        return str(self._Property('STATUS'))

    Status = property(_GetStatus,
    doc="""Status.

    :type: `enums`.chs*
    """)

    def _GetTimestamp(self):
        return float(self._Property('TIMESTAMP'))

    Timestamp = property(_GetTimestamp,
    doc="""Chat timestamp.

    :type: float

    :see: `Datetime`
    """)

    # Note. When TOPICXML is set, the value is stripped of XML tags and updated in TOPIC.

    def _GetTopic(self):
        return self._Property('TOPIC')

    def _SetTopic(self, Value):
        self._Alter('SETTOPIC', tounicode(Value))

    Topic = property(_GetTopic, _SetTopic,
    doc="""Chat topic.

    :type: unicode
    """)

    def _GetTopicXML(self):
        return self._Property('TOPICXML')

    def _SetTopicXML(self, Value):
        self._Alter('SETTOPICXML', tounicode(Value))

    TopicXML = property(_GetTopicXML, _SetTopicXML,
    doc="""Chat topic in XML format.

    :type: unicode
    """)

    def _GetType(self):
        return str(self._Property('TYPE'))

    Type = property(_GetType,
    doc="""Chat type.

    :type: `enums`.chatType*
    """)


class ChatCollection(CachedCollection):
    _CachedType = Chat


class ChatMessage(Cached):
    """Represents a single chat message.
    """
    _ValidateHandle = int

    def __repr__(self):
        return Cached.__repr__(self, 'Id')

    def _Property(self, PropName, Value=None, Cache=True):
        return self._Owner._Property('CHATMESSAGE', self.Id, PropName, Value, Cache)

    def MarkAsSeen(self):
        """Marks a missed chat message as seen.
        """
        self._Owner._DoCommand('SET CHATMESSAGE %d SEEN' % self.Id, 'CHATMESSAGE %d STATUS READ' % self.Id)

    def _GetBody(self):
        return self._Property('BODY')

    def _SetBody(self, Value):
        self._Property('BODY', tounicode(Value))

    Body = property(_GetBody, _SetBody,
    doc="""Chat message body.

    :type: unicode
    """)

    def _GetChat(self):
        return Chat(self._Owner, self.ChatName)

    Chat = property(_GetChat,
    doc="""Chat this message was posted on.

    :type: `Chat`
    """)

    def _GetChatName(self):
        return str(self._Property('CHATNAME'))

    ChatName = property(_GetChatName,
    doc="""Name of the chat this message was posted on.

    :type: str
    """)

    def _GetDatetime(self):
        from datetime import datetime
        return datetime.fromtimestamp(self.Timestamp)

    Datetime = property(_GetDatetime,
    doc="""Chat message timestamp as datetime.

    :type: datetime.datetime
    """)

    def _GetEditedBy(self):
        return str(self._Property('EDITED_BY'))

    EditedBy = property(_GetEditedBy,
    doc="""Skypename of the user who edited this message.

    :type: str
    """)

    def _GetEditedDatetime(self):
        from datetime import datetime
        return datetime.fromtimestamp(self.EditedTimestamp)

    EditedDatetime = property(_GetEditedDatetime,
    doc="""Message editing timestamp as datetime.

    :type: datetime.datetime
    """)

    def _GetEditedTimestamp(self):
        return float(self._Property('EDITED_TIMESTAMP'))

    EditedTimestamp = property(_GetEditedTimestamp,
    doc="""Message editing timestamp.

    :type: float
    """)

    def _GetFromDisplayName(self):
        return self._Property('FROM_DISPNAME')

    FromDisplayName = property(_GetFromDisplayName,
    doc="""DisplayName of the message sender.

    :type: unicode
    """)

    def _GetFromHandle(self):
        return str(self._Property('FROM_HANDLE'))

    FromHandle = property(_GetFromHandle,
    doc="""Skypename of the message sender.

    :type: str
    """)

    def _GetId(self):
        return self._Handle

    Id = property(_GetId,
    doc="""Chat message Id.

    :type: int
    """)

    def _GetIsEditable(self):
        return (self._Property('IS_EDITABLE') == 'TRUE')

    IsEditable = property(_GetIsEditable,
    doc="""Tells if message body is editable.

    :type: bool
    """)

    def _GetLeaveReason(self):
        return str(self._Property('LEAVEREASON'))

    LeaveReason = property(_GetLeaveReason,
    doc="""LeaveReason.

    :type: `enums`.lea*
    """)

    def _SetSeen(self, Value):
        from warnings import warn
        warn('ChatMessage.Seen = x: Use ChatMessage.MarkAsSeen() instead.', DeprecationWarning, stacklevel=2)
        if Value:
            self.MarkAsSeen()
        else:
            raise SkypeError(0, 'Seen can only be set to True')

    Seen = property(fset=_SetSeen,
    doc="""Marks a missed chat message as seen. Accepts only True value.

    :type: bool

    :deprecated: Extremely unpythonic, use `MarkAsSeen` instead.
    """)

    def _GetSender(self):
        return User(self._Owner, self.FromHandle)

    Sender = property(_GetSender,
    doc="""Sender of the chat message.

    :type: `User`
    """)

    def _GetStatus(self):
        return str(self._Property('STATUS'))

    Status = property(_GetStatus,
    doc="""Status of the chat message.

    :type: `enums`.cms*
    """)

    def _GetTimestamp(self):
        return float(self._Property('TIMESTAMP'))

    Timestamp = property(_GetTimestamp,
    doc="""Chat message timestamp.

    :type: float

    :see: `Datetime`
    """)

    def _GetType(self):
        return str(self._Property('TYPE'))

    Type = property(_GetType,
    doc="""Type of chat message.

    :type: `enums`.cme*
    """)

    def _GetUsers(self):
        return UserCollection(self._Owner, split(self._Property('USERS')))

    Users = property(_GetUsers,
    doc="""Users added to the chat.

    :type: `UserCollection`
    """)


class ChatMessageCollection(CachedCollection):
    _CachedType = ChatMessage


class ChatMember(Cached):
    """Represents a member of a public chat.
    """
    _ValidateHandle = int

    def __repr__(self):
        return Cached.__repr__(self, 'Id')

    def _Alter(self, AlterName, Args=None):
        return self._Owner._Alter('CHATMEMBER', self.Id, AlterName, Args,
                                  'ALTER CHATMEMBER %s %s' % (self.Id, AlterName))

    def _Property(self, PropName, Value=None, Cache=True):
        return self._Owner._Property('CHATMEMBER', self.Id, PropName, Value, Cache)

    def CanSetRoleTo(self, Role):
        """Checks if the new role can be applied to the member.

        :Parameters:
          Role : `enums`.chatMemberRole*
            New chat member role.

        :return: True if the new role can be applied, False otherwise.
        :rtype: bool
        """
        t = self._Owner._Alter('CHATMEMBER', self.Id, 'CANSETROLETO', Role,
                               'ALTER CHATMEMBER CANSETROLETO')
        return (chop(t, 1)[-1] == 'TRUE')

    def _GetChat(self):
        return Chat(self._Owner, self._Property('CHATNAME'))

    Chat = property(_GetChat,
    doc="""Chat this member belongs to.

    :type: `Chat`
    """)

    def _GetHandle(self):
        return str(self._Property('IDENTITY'))

    Handle = property(_GetHandle,
    doc="""Member Skypename.

    :type: str
    """)

    def _GetId(self):
        return self._Handle

    Id = property(_GetId,
    doc="""Chat member Id.

    :type: int
    """)

    def _GetIsActive(self):
        return (self._Property('IS_ACTIVE') == 'TRUE')

    IsActive = property(_GetIsActive,
    doc="""Member activity status.

    :type: bool
    """)

    def _GetRole(self):
        return str(self._Property('ROLE'))

    def _SetRole(self, Value):
        self._Alter('SETROLETO', Value)

    Role = property(_GetRole, _SetRole,
    doc="""Chat Member role.

    :type: `enums`.chatMemberRole*
    """)


class ChatMemberCollection(CachedCollection):
    _CachedType = ChatMember
