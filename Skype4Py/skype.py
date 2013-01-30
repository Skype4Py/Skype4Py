"""Main Skype interface.
"""
__docformat__ = 'restructuredtext en'


import threading
import weakref
import logging

from api import *
from errors import *
from enums import *
from utils import *
from conversion import *
from client import *
from user import *
from call import *
from profile import *
from settings import *
from chat import *
from application import *
from voicemail import *
from sms import *
from filetransfer import *


class APINotifier(SkypeAPINotifier):
    def __init__(self, skype):
        self.skype = weakref.proxy(skype)

    def attachment_changed(self, status):
        try:
            self.skype._CallEventHandler('AttachmentStatus', status)
            if status == apiAttachRefused:
                raise SkypeAPIError('Skype connection refused')
        except weakref.ReferenceError:
            pass

    def notification_received(self, notification):
        try:
            skype = self.skype
            skype._CallEventHandler('Notify', notification)
            a, b = chop(notification)
            object_type = None
            # if..elif handling cache and most event handlers
            if a in ('CALL', 'USER', 'GROUP', 'CHAT', 'CHATMESSAGE', 'CHATMEMBER', 'VOICEMAIL', 'APPLICATION', 'SMS', 'FILETRANSFER'):
                object_type, object_id, prop_name, value = [a] + chop(b, 2)
                skype._CacheDict[str(object_type), str(object_id), str(prop_name)] = value
                if object_type == 'USER':
                    o = User(skype, object_id)
                    if prop_name == 'ONLINESTATUS':
                        skype._CallEventHandler('OnlineStatus', o, str(value))
                    elif prop_name == 'MOOD_TEXT' or prop_name == 'RICH_MOOD_TEXT':
                        skype._CallEventHandler('UserMood', o, value)
                    elif prop_name == 'RECEIVEDAUTHREQUEST':
                        skype._CallEventHandler('UserAuthorizationRequestReceived', o)
                elif object_type == 'CALL':
                    o = Call(skype, object_id)
                    if prop_name == 'STATUS':
                        skype._CallEventHandler('CallStatus', o, str(value))
                    elif prop_name == 'SEEN':
                        skype._CallEventHandler('CallSeenStatusChanged', o, (value == 'TRUE'))
                    elif prop_name == 'VAA_INPUT_STATUS':
                        skype._CallEventHandler('CallInputStatusChanged', o, (value == 'TRUE'))
                    elif prop_name == 'TRANSFER_STATUS':
                        skype._CallEventHandler('CallTransferStatusChanged', o, str(value))
                    elif prop_name == 'DTMF':
                        skype._CallEventHandler('CallDtmfReceived', o, str(value))
                    elif prop_name == 'VIDEO_STATUS':
                        skype._CallEventHandler('CallVideoStatusChanged', o, str(value))
                    elif prop_name == 'VIDEO_SEND_STATUS':
                        skype._CallEventHandler('CallVideoSendStatusChanged', o, str(value))
                    elif prop_name == 'VIDEO_RECEIVE_STATUS':
                        skype._CallEventHandler('CallVideoReceiveStatusChanged', o, str(value))
                elif object_type == 'CHAT':
                    o = Chat(skype, object_id)
                    if prop_name == 'MEMBERS':
                        skype._CallEventHandler('ChatMembersChanged', o, UserCollection(skype, split(value)))
                    if prop_name in ('OPENED', 'CLOSED'):
                        skype._CallEventHandler('ChatWindowState', o, (prop_name == 'OPENED'))
                elif object_type == 'CHATMEMBER':
                    o = ChatMember(skype, object_id)
                    if prop_name == 'ROLE':
                        skype._CallEventHandler('ChatMemberRoleChanged', o, str(value))
                elif object_type == 'CHATMESSAGE':
                    o = ChatMessage(skype, object_id)
                    if prop_name == 'STATUS':
                        skype._CallEventHandler('MessageStatus', o, str(value))
                elif object_type == 'APPLICATION':
                    o = Application(skype, object_id)
                    if prop_name == 'CONNECTING':
                        skype._CallEventHandler('ApplicationConnecting', o, UserCollection(skype, split(value)))
                    elif prop_name == 'STREAMS':
                        skype._CallEventHandler('ApplicationStreams', o, ApplicationStreamCollection(o, split(value)))
                    elif prop_name == 'DATAGRAM':
                        handle, text = chop(value)
                        skype._CallEventHandler('ApplicationDatagram', o, ApplicationStream(o, handle), text)
                    elif prop_name == 'SENDING':
                        skype._CallEventHandler('ApplicationSending', o, ApplicationStreamCollection(o, (x.split('=')[0] for x in split(value))))
                    elif prop_name == 'RECEIVED':
                        skype._CallEventHandler('ApplicationReceiving', o, ApplicationStreamCollection(o, (x.split('=')[0] for x in split(value))))
                elif object_type == 'GROUP':
                    o = Group(skype, object_id)
                    if prop_name == 'VISIBLE':
                        skype._CallEventHandler('GroupVisible', o, (value == 'TRUE'))
                    elif prop_name == 'EXPANDED':
                        skype._CallEventHandler('GroupExpanded', o, (value == 'TRUE'))
                    elif prop_name == 'NROFUSERS':
                        skype._CallEventHandler('GroupUsers', o, int(value))
                elif object_type == 'SMS':
                    o = SmsMessage(skype, object_id)
                    if prop_name == 'STATUS':
                        skype._CallEventHandler('SmsMessageStatusChanged', o, str(value))
                    elif prop_name == 'TARGET_STATUSES':
                        for t in split(value, ', '):
                            number, status = t.split('=')
                            skype._CallEventHandler('SmsTargetStatusChanged', SmsTarget(o, number), str(status))
                elif object_type == 'FILETRANSFER':
                    o = FileTransfer(skype, object_id)
                    if prop_name == 'STATUS':
                        skype._CallEventHandler('FileTransferStatusChanged', o, str(value))
                elif object_type == 'VOICEMAIL':
                    o = Voicemail(skype, object_id)
                    if prop_name == 'STATUS':
                        skype._CallEventHandler('VoicemailStatus', o, str(value))
            elif a in ('PROFILE', 'PRIVILEGE'):
                object_type, object_id, prop_name, value = [a, ''] + chop(b)
                skype._CacheDict[str(object_type), str(object_id), str(prop_name)] = value
            elif a in ('CURRENTUSERHANDLE', 'USERSTATUS', 'CONNSTATUS', 'PREDICTIVE_DIALER_COUNTRY', 'SILENT_MODE', 'AUDIO_IN', 'AUDIO_OUT', 'RINGER', 'MUTE', 'AUTOAWAY', 'WINDOWSTATE'):
                object_type, object_id, prop_name, value = [a, '', '', b]
                skype._CacheDict[str(object_type), str(object_id), str(prop_name)] = value
                if object_type == 'MUTE':
                    skype._CallEventHandler('Mute', value == 'TRUE')
                elif object_type == 'CONNSTATUS':
                    skype._CallEventHandler('ConnectionStatus', str(value))
                elif object_type == 'USERSTATUS':
                    skype._CallEventHandler('UserStatus', str(value))
                elif object_type == 'AUTOAWAY':
                    skype._CallEventHandler('AutoAway', (value == 'ON'))
                elif object_type == 'WINDOWSTATE':
                    skype._CallEventHandler('ClientWindowState', str(value))
                elif object_type == 'SILENT_MODE':
                    skype._CallEventHandler('SilentModeStatusChanged', (value == 'ON'))
            elif a == 'CALLHISTORYCHANGED':
                skype._CallEventHandler('CallHistory')
            elif a == 'IMHISTORYCHANGED':
                skype._CallEventHandler('MessageHistory', '') # XXX: Arg is Skypename, which one?
            elif a == 'CONTACTS':
                prop_name, value = chop(b)
                if prop_name == 'FOCUSED':
                    skype._CallEventHandler('ContactsFocused', str(value))
            elif a == 'DELETED':
                prop_name, value = chop(b)
                if prop_name == 'GROUP':
                    skype._CallEventHandler('GroupDeleted', int(value))
            elif a == 'EVENT':
                object_id, prop_name, value = chop(b, 2)
                if prop_name == 'CLICKED':
                    skype._CallEventHandler('PluginEventClicked', PluginEvent(skype, object_id))
            elif a == 'MENU_ITEM':
                object_id, prop_name, value = chop(b, 2)
                if prop_name == 'CLICKED':
                    i = value.rfind('CONTEXT ')
                    if i >= 0:
                        context = chop(value[i+8:])[0]
                        users = ()
                        context_id = u''
                        if context in (pluginContextContact, pluginContextCall, pluginContextChat):
                            users = UserCollection(skype, split(value[:i-1], ', '))
                        if context in (pluginContextCall, pluginContextChat):
                            j = value.rfind('CONTEXT_ID ')
                            if j >= 0:
                                context_id = str(chop(value[j+11:])[0])
                                if context == pluginContextCall:
                                    context_id = int(context_id)
                        skype._CallEventHandler('PluginMenuItemClicked', PluginMenuItem(skype, object_id), users, str(context), context_id)
            elif a == 'WALLPAPER':
                skype._CallEventHandler('WallpaperChanged', unicode2path(b))
        except weakref.ReferenceError:
            pass

    def sending_command(self, command):
        try:
            self.skype._CallEventHandler('Command', command)
        except weakref.ReferenceError:
            pass

    def reply_received(self, command):
        try:
            self.skype._CallEventHandler('Reply', command)
        except weakref.ReferenceError:
            pass


class Skype(EventHandlingBase):
    """The main class which you have to instantiate to get access to the Skype client
    running currently in the background.

    Usage
    =====

       You should access this class using the alias at the package level:

       .. python::

           import Skype4Py

           skype = Skype4Py.Skype()

       Read the constructor (`Skype.__init__`) documentation for a list of accepted
       arguments.

    Events
    ======

       This class provides events.

       The events names and their arguments lists can be found in the `SkypeEvents`
       class in this module.

       The use of events is explained in the `EventHandlingBase` class
       which is a superclass of this class.
    """

    def __init__(self, Events=None, **Options):
        """Initializes the object.

        :Parameters:
          Events
            An optional object with event handlers. See `Skype4Py.utils.EventHandlingBase`
            for more information on events.
          Options
            Additional options for low-level API handler. See the `Skype4Py.api`
            subpackage for supported options. Available options may depend on the
            current platform. Note that the current platform can be queried using
            `Skype4Py.platform` variable.
        """
        self._Logger = logging.getLogger('Skype4Py.skype.Skype')
        self._Logger.info('object created')

        EventHandlingBase.__init__(self)
        if Events:
            self._SetEventHandlerObject(Events)

        try:
            self._Api = Options.pop('Api')
            if Options:
                raise TypeError('No options supported with custom API objects.')
        except KeyError:
            self._Api = SkypeAPI(Options)
        self._Api.set_notifier(APINotifier(self))

        Cached._CreateOwner(self)

        self._Cache = True
        self.ResetCache()

        from api import DEFAULT_TIMEOUT
        self._Timeout = DEFAULT_TIMEOUT

        self._Convert = Conversion(self)
        self._Client = Client(self)
        self._Settings = Settings(self)
        self._Profile = Profile(self)

    def __del__(self):
        """Frees all resources.
        """
        if hasattr(self, '_Api'):
            self._Api.close()

        self._Logger.info('object destroyed')

    def _DoCommand(self, Cmd, ExpectedReply=''):
        command = Command(Cmd, ExpectedReply, True, self.Timeout)
        self.SendCommand(command)
        a, b = chop(command.Reply)
        if a == 'ERROR':
            errnum, errstr = chop(b)
            self._CallEventHandler('Error', command, int(errnum), errstr)
            raise SkypeError(int(errnum), errstr)
        if not command.Reply.startswith(command.Expected):
            raise SkypeError(0, 'Unexpected reply from Skype, got [%s], expected [%s (...)]' % \
                (command.Reply, command.Expected))
        return command.Reply

    def _Property(self, ObjectType, ObjectId, PropName, Set=None, Cache=True):
        h = (str(ObjectType), str(ObjectId), str(PropName))
        arg = ('%s %s %s' % h).split()
        while '' in arg:
            arg.remove('')
        jarg = ' '.join(arg)
        if Set is None: # Get
            if Cache and self._Cache and h in self._CacheDict:
                return self._CacheDict[h]
            value = self._DoCommand('GET %s' % jarg, jarg)
            while arg:
                try:
                    a, b = chop(value)
                except ValueError:
                    break
                if a.lower() != arg[0].lower():
                    break
                del arg[0]
                value = b
            if Cache and self._Cache:
                self._CacheDict[h] = value
            return value
        else: # Set
            value = unicode(Set)
            self._DoCommand('SET %s %s' % (jarg, value), jarg)
            if Cache and self._Cache:
                self._CacheDict[h] = value

    def _Alter(self, ObjectType, ObjectId, AlterName, Args=None, Reply=None):
        cmd = 'ALTER %s %s %s' % (str(ObjectType), str(ObjectId), str(AlterName))
        if Reply is None:
            Reply = cmd
        if Args is not None:
            cmd = '%s %s' % (cmd, tounicode(Args))
        reply = self._DoCommand(cmd, Reply)
        arg = cmd.split()
        while arg:
            try:
                a, b = chop(reply)
            except ValueError:
                break
            if a.lower() != arg[0].lower():
                break
            del arg[0]
            reply = b
        return reply

    def _Search(self, ObjectType, Args=None):
        cmd = 'SEARCH %s' % ObjectType
        if Args is not None:
            cmd = '%s %s' % (cmd, Args)
        # It is safe to do str() as none of the searchable objects use non-ascii chars.
        return split(chop(str(self._DoCommand(cmd)))[-1], ', ')

    def ApiSecurityContextEnabled(self, Context):
        """Queries if an API security context for Internet Explorer is enabled.

        :Parameters:
          Context : unicode
            API security context to check.

        :return: True if the API security for the given context is enabled, False otherwise.
        :rtype: bool

        :warning: This functionality isn't supported by Skype4Py.
        """
        self._Api.security_context_enabled(Context)

    def Application(self, Name):
        """Queries an application object.

        :Parameters:
          Name : unicode
            Application name.

        :return: The application object.
        :rtype: `application.Application`
        """
        return Application(self, Name)

    def _AsyncSearchUsersReplyHandler(self, Command):
        if Command in self._AsyncSearchUsersCommands:
            self._AsyncSearchUsersCommands.remove(Command)
            self._CallEventHandler('AsyncSearchUsersFinished', Command.Id,
                UserCollection(self, split(chop(Command.Reply)[-1], ', ')))
            if len(self._AsyncSearchUsersCommands) == 0:
                self.UnregisterEventHandler('Reply', self._AsyncSearchUsersReplyHandler)
                del self._AsyncSearchUsersCommands

    def AsyncSearchUsers(self, Target):
        """Asynchronously searches for Skype users.

        :Parameters:
          Target : unicode
            Search target (name or email address).

        :return: A search identifier. It will be passed along with the results to the
                 `SkypeEvents.AsyncSearchUsersFinished` event after the search is completed.
        :rtype: int
        """
        if not hasattr(self, '_AsyncSearchUsersCommands'):
            self._AsyncSearchUsersCommands = []
            self.RegisterEventHandler('Reply', self._AsyncSearchUsersReplyHandler)
        command = Command('SEARCH USERS %s' % tounicode(Target), 'USERS', False, self.Timeout)
        self._AsyncSearchUsersCommands.append(command)
        self.SendCommand(command)
        # return pCookie - search identifier
        return command.Id

    def Attach(self, Protocol=5, Wait=True):
        """Establishes a connection to Skype.

        :Parameters:
          Protocol : int
            Minimal Skype protocol version.
          Wait : bool
            If set to False, blocks forever until the connection is established. Otherwise, timeouts
            after the `Timeout`.
        """
        try:
            self._Api.protocol = Protocol
            self._Api.attach(self.Timeout, Wait)
        except SkypeAPIError:
            self.ResetCache()
            raise

    def Call(self, Id=0):
        """Queries a call object.

        :Parameters:
          Id : int
            Call identifier.

        :return: Call object.
        :rtype: `call.Call`
        """
        o = Call(self, Id)
        o.Status # Test if such a call exists.
        return o

    def Calls(self, Target=''):
        """Queries calls in call history.

        :Parameters:
          Target : str
            Call target.

        :return: Call objects.
        :rtype: `CallCollection`
        """
        return CallCollection(self, self._Search('CALLS', Target))

    def _ChangeUserStatus_UserStatus(self, Status):
        if Status.upper() == self._ChangeUserStatus_Status:
            self._ChangeUserStatus_Event.set()

    def ChangeUserStatus(self, Status):
        """Changes the online status for the current user.

        :Parameters:
          Status : `enums`.cus*
            New online status for the user.

        :note: This function waits until the online status changes. Alternatively, use the
               `CurrentUserStatus` property to perform an immediate change of status.
        """
        if self.CurrentUserStatus.upper() == Status.upper():
            return
        self._ChangeUserStatus_Event = threading.Event()
        self._ChangeUserStatus_Status = Status.upper()
        self.RegisterEventHandler('UserStatus', self._ChangeUserStatus_UserStatus)
        self.CurrentUserStatus = Status
        self._ChangeUserStatus_Event.wait()
        self.UnregisterEventHandler('UserStatus', self._ChangeUserStatus_UserStatus)
        del self._ChangeUserStatus_Event, self._ChangeUserStatus_Status

    def Chat(self, Name=''):
        """Queries a chat object.

        :Parameters:
          Name : str
            Chat name.

        :return: A chat object.
        :rtype: `chat.Chat`
        """
        o = Chat(self, Name)
        o.Status # Tests if such a chat really exists.
        return o

    def ClearCallHistory(self, Username='ALL', Type=chsAllCalls):
        """Clears the call history.

        :Parameters:
          Username : str
            Skypename of the user. A special value of 'ALL' means that entries of all users should
            be removed.
          Type : `enums`.clt*
            Call type.
        """
        cmd = 'CLEAR CALLHISTORY %s %s' % (str(Type), Username)
        self._DoCommand(cmd, cmd)

    def ClearChatHistory(self):
        """Clears the chat history.
        """
        cmd = 'CLEAR CHATHISTORY'
        self._DoCommand(cmd, cmd)

    def ClearVoicemailHistory(self):
        """Clears the voicemail history.
        """
        self._DoCommand('CLEAR VOICEMAILHISTORY')

    def Command(self, Command, Reply=u'', Block=False, Timeout=30000, Id=-1):
        """Creates an API command object.

        :Parameters:
          Command : unicode
            Command string.
          Reply : unicode
            Expected reply. By default any reply is accepted (except errors which raise an
            `SkypeError` exception).
          Block : bool
            If set to True, `SendCommand` method waits for a response from Skype API before
            returning.
          Timeout : float, int or long
            Timeout. Used if Block == True. Timeout may be expressed in milliseconds if the type
            is int or long or in seconds (or fractions thereof) if the type is float.
          Id : int
            Command Id. The default (-1) means it will be assigned automatically as soon as the
            command is sent.

        :return: A command object.
        :rtype: `Command`

        :see: `SendCommand`
        """
        from api import Command as CommandClass
        return CommandClass(Command, Reply, Block, Timeout, Id)

    def Conference(self, Id=0):
        """Queries a call conference object.

        :Parameters:
          Id : int
            Conference Id.

        :return: A conference object.
        :rtype: `Conference`
        """
        o = Conference(self, Id)
        if Id <= 0 or not o.Calls:
            raise SkypeError(0, 'Unknown conference')
        return o

    def CreateChatUsingBlob(self, Blob):
        """Returns existing or joins a new chat using given blob.

        :Parameters:
          Blob : str
            A blob identifying the chat.

        :return: A chat object
        :rtype: `chat.Chat`
        """
        return Chat(self, chop(self._DoCommand('CHAT CREATEUSINGBLOB %s' % Blob), 2)[1])

    def CreateChatWith(self, *Usernames):
        """Creates a chat with one or more users.

        :Parameters:
          Usernames : str
            One or more Skypenames of the users.

        :return: A chat object
        :rtype: `Chat`

        :see: `Chat.AddMembers`
        """
        return Chat(self, chop(self._DoCommand('CHAT CREATE %s' % ', '.join(Usernames)), 2)[1])

    def CreateGroup(self, GroupName):
        """Creates a custom contact group.

        :Parameters:
          GroupName : unicode
            Group name.

        :return: A group object.
        :rtype: `Group`

        :see: `DeleteGroup`
        """
        groups = self.CustomGroups
        self._DoCommand('CREATE GROUP %s' % tounicode(GroupName))
        for g in self.CustomGroups:
            if g not in groups and g.DisplayName == GroupName:
                return g
        raise SkypeError(0, 'Group creating failed')

    def CreateSms(self, MessageType, *TargetNumbers):
        """Creates an SMS message.

        :Parameters:
          MessageType : `enums`.smsMessageType*
            Message type.
          TargetNumbers : str
            One or more target SMS numbers.

        :return: An sms message object.
        :rtype: `SmsMessage`
        """
        return SmsMessage(self, chop(self._DoCommand('CREATE SMS %s %s' % (MessageType, ', '.join(TargetNumbers))), 2)[1])

    def DeleteGroup(self, GroupId):
        """Deletes a custom contact group.

        Users in the contact group are moved to the All Contacts (hardwired) contact group.

        :Parameters:
          GroupId : int
            Group identifier. Get it from `Group.Id`.

        :see: `CreateGroup`
        """
        self._DoCommand('DELETE GROUP %s' % GroupId)

    def EnableApiSecurityContext(self, Context):
        """Enables an API security context for Internet Explorer scripts.

        :Parameters:
          Context : unicode
            combination of API security context values.

        :warning: This functionality isn't supported by Skype4Py.
        """
        self._Api.enable_security_context(Context)

    def FindChatUsingBlob(self, Blob):
        """Returns existing chat using given blob.

        :Parameters:
          Blob : str
            A blob identifying the chat.

        :return: A chat object
        :rtype: `chat.Chat`
        """
        return Chat(self, chop(self._DoCommand('CHAT FINDUSINGBLOB %s' % Blob), 2)[1])

    def Greeting(self, Username=''):
        """Queries the greeting used as voicemail.

        :Parameters:
          Username : str
            Skypename of the user.

        :return: A voicemail object.
        :rtype: `Voicemail`
        """
        for v in self.Voicemails:
            if Username and v.PartnerHandle != Username:
                continue
            if v.Type in (vmtDefaultGreeting, vmtCustomGreeting):
                return v

    def Message(self, Id=0):
        """Queries a chat message object.

        :Parameters:
          Id : int
            Message Id.

        :return: A chat message object.
        :rtype: `ChatMessage`
        """
        o = ChatMessage(self, Id)
        o.Status # Test if such an id is known.
        return o

    def Messages(self, Target=''):
        """Queries chat messages which were sent/received by the user.

        :Parameters:
          Target : str
            Message sender.

        :return: Chat message objects.
        :rtype: `ChatMessageCollection`
        """
        return ChatMessageCollection(self, self._Search('CHATMESSAGES', Target))

    def PlaceCall(self, *Targets):
        """Places a call to a single user or creates a conference call.

        :Parameters:
          Targets : str
            One or more call targets. If multiple targets are specified, a conference call is
            created. The call target can be a Skypename, phone number, or speed dial code.

        :return: A call object.
        :rtype: `call.Call`
        """
        calls = self.ActiveCalls
        reply = self._DoCommand('CALL %s' % ', '.join(Targets))
        # Skype for Windows returns the call status which gives us the call Id;
        if reply.startswith('CALL '):
            return Call(self, chop(reply, 2)[1])
        # On linux we get 'OK' as reply so we search for the new call on
        # list of active calls.
        for c in self.ActiveCalls:
            if c not in calls:
                return c
        raise SkypeError(0, 'Placing call failed')

    def Privilege(self, Name):
        """Queries the Skype services (privileges) enabled for the Skype client.

        :Parameters:
          Name : str
            Privilege name, currently one of 'SKYPEOUT', 'SKYPEIN', 'VOICEMAIL'.

        :return: True if the privilege is available, False otherwise.
        :rtype: bool
        """
        return (self._Property('PRIVILEGE', '', Name.upper()) == 'TRUE')

    def Profile(self, Property, Set=None):
        """Queries/sets user profile properties.

        :Parameters:
          Property : str
            Property name, currently one of 'PSTN_BALANCE', 'PSTN_BALANCE_CURRENCY', 'FULLNAME',
            'BIRTHDAY', 'SEX', 'LANGUAGES', 'COUNTRY', 'PROVINCE', 'CITY', 'PHONE_HOME',
            'PHONE_OFFICE', 'PHONE_MOBILE', 'HOMEPAGE', 'ABOUT'.
          Set : unicode or None
            Value the property should be set to or None if the value should be queried.

        :return: Property value if Set=None, None otherwise.
        :rtype: unicode or None
        """
        return self._Property('PROFILE', '', Property, Set)

    def Property(self, ObjectType, ObjectId, PropName, Set=None):
        """Queries/sets the properties of an object.

        :Parameters:
          ObjectType : str
            Object type ('USER', 'CALL', 'CHAT', 'CHATMESSAGE', ...).
          ObjectId : str
            Object Id, depends on the object type.
          PropName : str
            Name of the property to access.
          Set : unicode or None
            Value the property should be set to or None if the value should be queried.

        :return: Property value if Set=None, None otherwise.
        :rtype: unicode or None
        """
        return self._Property(ObjectType, ObjectId, PropName, Set)

    def ResetCache(self):
        """Deletes all command cache entries.

        This method clears the Skype4Py's internal command cache which means that all objects will forget
        their property values and querying them will trigger a code to get them from Skype client (and
        cache them again).
        """
        self._CacheDict = {}

    def SearchForUsers(self, Target):
        """Searches for users.

        :Parameters:
          Target : unicode
            Search target (name or email address).

        :return: Found users.
        :rtype: `UserCollection`
        """
        return UserCollection(self, self._Search('USERS', tounicode(Target)))

    def SendCommand(self, Command):
        """Sends an API command.

        :Parameters:
          Command : `Command`
            Command to send. Use `Command` method to create a command.
        """
        try:
            self._Api.send_command(Command)
        except SkypeAPIError:
            self.ResetCache()
            raise

    def SendMessage(self, Username, Text):
        """Sends a chat message.

        :Parameters:
          Username : str
            Skypename of the user.
          Text : unicode
            Body of the message.

        :return: A chat message object.
        :rtype: `ChatMessage`
        """
        return self.CreateChatWith(Username).SendMessage(Text)

    def SendSms(self, *TargetNumbers, **Properties):
        """Creates and sends an SMS message.

        :Parameters:
          TargetNumbers : str
            One or more target SMS numbers.
          Properties
            Message properties. Properties available are same as `SmsMessage` object properties.

        :return: An sms message object. The message is already sent at this point.
        :rtype: `SmsMessage`
        """
        sms = self.CreateSms(smsMessageTypeOutgoing, *TargetNumbers)
        for name, value in Properties.items():
            if isinstance(getattr(sms.__class__, name, None), property):
                setattr(sms, name, value)
            else:
                raise TypeError('Unknown property: %s' % prop)
        sms.Send()
        return sms

    def SendVoicemail(self, Username):
        """Sends a voicemail to a specified user.

        :Parameters:
          Username : str
            Skypename of the user.

        :note: Should return a `Voicemail` object. This is not implemented yet.
        """
        if self._Api.protocol >= 6:
            self._DoCommand('CALLVOICEMAIL %s' % Username)
        else:
            self._DoCommand('VOICEMAIL %s' % Username)

    def User(self, Username=''):
        """Queries a user object.

        :Parameters:
          Username : str
            Skypename of the user.

        :return: A user object.
        :rtype: `user.User`
        """
        if not Username:
            Username = self.CurrentUserHandle
        o = User(self, Username)
        o.OnlineStatus # Test if such a user exists.
        return o

    def Variable(self, Name, Set=None):
        """Queries/sets Skype general parameters.

        :Parameters:
          Name : str
            Variable name.
          Set : unicode or None
            Value the variable should be set to or None if the value should be queried.

        :return: Variable value if Set=None, None otherwise.
        :rtype: unicode or None
        """
        return self._Property(Name, '', '', Set)

    def Voicemail(self, Id):
        """Queries the voicemail object.

        :Parameters:
          Id : int
            Voicemail Id.

        :return: A voicemail object.
        :rtype: `Voicemail`
        """
        o = Voicemail(self, Id)
        o.Type # Test if such a voicemail exists.
        return o

    def _GetActiveCalls(self):
        return CallCollection(self, self._Search('ACTIVECALLS'))

    ActiveCalls = property(_GetActiveCalls,
    doc="""Queries a list of active calls.

    :type: `CallCollection`
    """)

    def _GetActiveChats(self):
        return ChatCollection(self, self._Search('ACTIVECHATS'))

    ActiveChats = property(_GetActiveChats,
    doc="""Queries a list of active chats.

    :type: `ChatCollection`
    """)

    def _GetActiveFileTransfers(self):
        return FileTransferCollection(self, self._Search('ACTIVEFILETRANSFERS'))

    ActiveFileTransfers = property(_GetActiveFileTransfers,
    doc="""Queries currently active file transfers.

    :type: `FileTransferCollection`
    """)

    def _GetApiWrapperVersion(self):
        import pkg_resources
        return pkg_resources.get_distribution("Skype4Py").version

    ApiWrapperVersion = property(_GetApiWrapperVersion,
    doc="""Returns Skype4Py version.

    :type: str
    """)

    def _GetAttachmentStatus(self):
        return self._Api.attachment_status

    AttachmentStatus = property(_GetAttachmentStatus,
    doc="""Queries the attachment status of the Skype client.

    :type: `enums`.apiAttach*
    """)

    def _GetBookmarkedChats(self):
        return ChatCollection(self, self._Search('BOOKMARKEDCHATS'))

    BookmarkedChats = property(_GetBookmarkedChats,
    doc="""Queries a list of bookmarked chats.

    :type: `ChatCollection`
    """)

    def _GetCache(self):
        return self._Cache

    def _SetCache(self, Value):
        self._Cache = bool(Value)

    Cache = property(_GetCache, _SetCache,
    doc="""Queries/sets the status of internal cache. The internal API cache is used
    to cache Skype object properties and global parameters.

    :type: bool
    """)

    def _GetChats(self):
        return ChatCollection(self, self._Search('CHATS'))

    Chats = property(_GetChats,
    doc="""Queries a list of chats.

    :type: `ChatCollection`
    """)

    def _GetClient(self):
        return self._Client

    Client = property(_GetClient,
    doc="""Queries the user interface control object.

    :type: `Client`
    """)

    def _GetCommandId(self):
        return True

    def _SetCommandId(self, Value):
        if not Value:
            raise SkypeError(0, 'CommandId may not be False')

    CommandId = property(_GetCommandId, _SetCommandId,
    doc="""Queries/sets the status of automatic command identifiers.

    :type: bool

    :note: Currently the only supported value is True.
    """)

    def _GetConferences(self):
        cids = []
        for c in self.Calls():
            cid = c.ConferenceId
            if cid > 0 and cid not in cids:
                cids.append(cid)
        return ConferenceCollection(self, cids)

    Conferences = property(_GetConferences,
    doc="""Queries a list of call conferences.

    :type: `ConferenceCollection`
    """)

    def _GetConnectionStatus(self):
        return str(self.Variable('CONNSTATUS'))

    ConnectionStatus = property(_GetConnectionStatus,
    doc="""Queries the connection status of the Skype client.

    :type: `enums`.con*
    """)

    def _GetConvert(self):
        return self._Convert

    Convert = property(_GetConvert,
    doc="""Queries the conversion object.

    :type: `Conversion`
    """)

    def _GetCurrentUser(self):
        return User(self, self.CurrentUserHandle)

    CurrentUser = property(_GetCurrentUser,
    doc="""Queries the current user object.

    :type: `user.User`
    """)

    def _GetCurrentUserHandle(self):
        return str(self.Variable('CURRENTUSERHANDLE'))

    CurrentUserHandle = property(_GetCurrentUserHandle,
    doc="""Queries the Skypename of the current user.

    :type: str
    """)

    def _GetCurrentUserProfile(self):
        return self._Profile

    CurrentUserProfile = property(_GetCurrentUserProfile,
    doc="""Queries the user profile object.

    :type: `Profile`
    """)

    def _GetCurrentUserStatus(self):
        return str(self.Variable('USERSTATUS'))

    def _SetCurrentUserStatus(self, Value):
        self.Variable('USERSTATUS', str(Value))

    CurrentUserStatus = property(_GetCurrentUserStatus, _SetCurrentUserStatus,
    doc="""Queries/sets the online status of the current user.

    :type: `enums`.ols*
    """)

    def _GetCustomGroups(self):
        return GroupCollection(self, self._Search('GROUPS', 'CUSTOM'))

    CustomGroups = property(_GetCustomGroups,
    doc="""Queries the list of custom contact groups. Custom groups are contact groups defined by the user.

    :type: `GroupCollection`
    """)

    def _GetFileTransfers(self):
        return FileTransferCollection(self, self._Search('FILETRANSFERS'))

    FileTransfers = property(_GetFileTransfers,
    doc="""Queries all file transfers.

    :type: `FileTransferCollection`
    """)

    def _GetFocusedContacts(self):
        # we have to use _DoCommand() directly because for unknown reason the API returns
        # "CONTACTS FOCUSED" instead of "CONTACTS_FOCUSED" (note the space instead of "_")
        return UserCollection(self, split(chop(self._DoCommand('GET CONTACTS_FOCUSED', 'CONTACTS FOCUSED'), 2)[-1]))

    FocusedContacts = property(_GetFocusedContacts,
    doc="""Queries a list of contacts selected in the contacts list.

    :type: `UserCollection`
    """)

    def _GetFriendlyName(self):
        return self._Api.friendly_name

    def _SetFriendlyName(self, Value):
        self._Api.set_friendly_name(tounicode(Value))

    FriendlyName = property(_GetFriendlyName, _SetFriendlyName,
    doc="""Queries/sets a "friendly" name for an application.

    :type: unicode
    """)

    def _GetFriends(self):
        return UserCollection(self, self._Search('FRIENDS'))

    Friends = property(_GetFriends,
    doc="""Queries the users in a contact list.

    :type: `UserCollection`
    """)

    def _GetGroups(self):
        return GroupCollection(self, self._Search('GROUPS', 'ALL'))

    Groups = property(_GetGroups,
    doc="""Queries the list of all contact groups.

    :type: `GroupCollection`
    """)

    def _GetHardwiredGroups(self):
        return GroupCollection(self, self._Search('GROUPS', 'HARDWIRED'))

    HardwiredGroups = property(_GetHardwiredGroups,
    doc="""Queries the list of hardwired contact groups. Hardwired groups are "smart" contact groups,
    defined by Skype, that cannot be removed.

    :type: `GroupCollection`
    """)

    def _GetMissedCalls(self):
        return CallCollection(self, self._Search('MISSEDCALLS'))

    MissedCalls = property(_GetMissedCalls,
    doc="""Queries a list of missed calls.

    :type: `CallCollection`
    """)

    def _GetMissedChats(self):
        return ChatCollection(self, self._Search('MISSEDCHATS'))

    MissedChats = property(_GetMissedChats,
    doc="""Queries a list of missed chats.

    :type: `ChatCollection`
    """)

    def _GetMissedMessages(self):
        return ChatMessageCollection(self, self._Search('MISSEDCHATMESSAGES'))

    MissedMessages = property(_GetMissedMessages,
    doc="""Queries a list of missed chat messages.

    :type: `ChatMessageCollection`
    """)

    def _GetMissedSmss(self):
        return SmsMessageCollection(self, self._Search('MISSEDSMSS'))

    MissedSmss = property(_GetMissedSmss,
    doc="""Requests a list of all missed SMS messages.

    :type: `SmsMessageCollection`
    """)

    def _GetMissedVoicemails(self):
        return VoicemailCollection(self, self._Search('MISSEDVOICEMAILS'))

    MissedVoicemails = property(_GetMissedVoicemails,
    doc="""Requests a list of missed voicemails.

    :type: `VoicemailCollection`
    """)

    def _GetMute(self):
        return self.Variable('MUTE') == 'ON'

    def _SetMute(self, Value):
        self.Variable('MUTE', cndexp(Value, 'ON', 'OFF'))

    Mute = property(_GetMute, _SetMute,
    doc="""Queries/sets the mute status of the Skype client.

    Type: bool
    Note: This value can be set only when there is an active call.

    :type: bool
    """)

    def _GetPredictiveDialerCountry(self):
        return str(self.Variable('PREDICTIVE_DIALER_COUNTRY'))

    PredictiveDialerCountry = property(_GetPredictiveDialerCountry,
    doc="""Returns predictive dialler country as an ISO code.

    :type: str
    """)

    def _GetProtocol(self):
        return self._Api.protocol

    def _SetProtocol(self, Value):
        self._DoCommand('PROTOCOL %s' % Value)
        self._Api.protocol = int(Value)

    Protocol = property(_GetProtocol, _SetProtocol,
    doc="""Queries/sets the protocol version used by the Skype client.

    :type: int
    """)

    def _GetRecentChats(self):
        return ChatCollection(self, self._Search('RECENTCHATS'))

    RecentChats = property(_GetRecentChats,
    doc="""Queries a list of recent chats.

    :type: `ChatCollection`
    """)

    def _GetSettings(self):
        return self._Settings

    Settings = property(_GetSettings,
    doc="""Queries the settings for Skype general parameters.

    :type: `Settings`
    """)

    def _GetSilentMode(self):
        return self._Property('SILENT_MODE', '', '', Cache=False) == 'ON'

    def _SetSilentMode(self, Value):
        self._Property('SILENT_MODE', '', '', cndexp(Value, 'ON', 'OFF'), Cache=False)

    SilentMode = property(_GetSilentMode, _SetSilentMode,
    doc="""Returns/sets Skype silent mode status.

    :type: bool
    """)

    def _GetSmss(self):
        return SmsMessageCollection(self, self._Search('SMSS'))

    Smss = property(_GetSmss,
    doc="""Requests a list of all SMS messages.

    :type: `SmsMessageCollection`
    """)

    def _GetTimeout(self):
        return self._Timeout

    def _SetTimeout(self, Value):
        if not isinstance(Value, (int, long, float)):
            raise TypeError('%s: wrong type, expected float (seconds), int or long (milliseconds)' %
                repr(type(Value)))
        self._Timeout = Value

    Timeout = property(_GetTimeout, _SetTimeout,
    doc="""Queries/sets the wait timeout value. This timeout value applies to every command sent
    to the Skype API and to attachment requests (see `Attach`). If a response is not received
    during the timeout period, an `SkypeAPIError` exception is raised.

    The units depend on the type. For float it is the number of seconds (or fractions thereof),
    for int or long it is the number of milliseconds. Floats are commonly used in Python modules
    to express timeouts (time.sleep() for example). Milliseconds are supported because that's
    what the Skype4COM library uses. Skype4Py support for real float timeouts was introduced
    in version 1.0.31.1.

    The default value is 30000 milliseconds (int).

    :type: float, int or long
    """)

    def _GetUsersWaitingAuthorization(self):
        return UserCollection(self, self._Search('USERSWAITINGMYAUTHORIZATION'))

    UsersWaitingAuthorization = property(_GetUsersWaitingAuthorization,
    doc="""Queries the list of users waiting for authorization.

    :type: `UserCollection`
    """)

    def _GetVersion(self):
        return str(self.Variable('SKYPEVERSION'))

    Version = property(_GetVersion,
    doc="""Queries the application version of the Skype client.

    :type: str
    """)

    def _GetVoicemails(self):
        return VoicemailCollection(self, self._Search('VOICEMAILS'))

    Voicemails = property(_GetVoicemails,
    doc="""Queries a list of voicemails.

    :type: `VoicemailCollection`
    """)


class SkypeEvents(object):
    """Events defined in `Skype`.

    See `EventHandlingBase` for more information on events.
    """

    def ApplicationConnecting(self, App, Users):
        """This event is triggered when list of users connecting to an application changes.

        :Parameters:
          App : `Application`
            Application object.
          Users : `UserCollection`
            Connecting users.
        """

    def ApplicationDatagram(self, App, Stream, Text):
        """This event is caused by the arrival of an application datagram.

        :Parameters:
          App : `Application`
            Application object.
          Stream : `ApplicationStream`
            Application stream that received the datagram.
          Text : unicode
            The datagram text.
        """

    def ApplicationReceiving(self, App, Streams):
        """This event is triggered when list of application receiving streams changes.

        :Parameters:
          App : `Application`
            Application object.
          Streams : `ApplicationStreamCollection`
            Application receiving streams.
        """

    def ApplicationSending(self, App, Streams):
        """This event is triggered when list of application sending streams changes.

        :Parameters:
          App : `Application`
            Application object.
          Streams : `ApplicationStreamCollection`
            Application sending streams.
        """

    def ApplicationStreams(self, App, Streams):
        """This event is triggered when list of application streams changes.

        :Parameters:
          App : `Application`
            Application object.
          Streams : `ApplicationStreamCollection`
            Application streams.
        """

    def AsyncSearchUsersFinished(self, Cookie, Users):
        """This event occurs when an asynchronous search is completed.

        :Parameters:
          Cookie : int
            Search identifier as returned by `Skype.AsyncSearchUsers`.
          Users : `UserCollection`
            Found users.

        :see: `Skype.AsyncSearchUsers`
        """

    def AttachmentStatus(self, Status):
        """This event is caused by a change in the status of an attachment to the Skype API.

        :Parameters:
          Status : `enums`.apiAttach*
            New attachment status.
        """

    def AutoAway(self, Automatic):
        """This event is caused by a change of auto away status.

        :Parameters:
          Automatic : bool
            New auto away status.
        """

    def CallDtmfReceived(self, Call, Code):
        """This event is caused by a call DTMF event.

        :Parameters:
          Call : `Call`
            Call object.
          Code : str
            Received DTMF code.
        """

    def CallHistory(self):
        """This event is caused by a change in call history.
        """

    def CallInputStatusChanged(self, Call, Active):
        """This event is caused by a change in the Call voice input status change.

        :Parameters:
          Call : `Call`
            Call object.
          Active : bool
            New voice input status (active when True).
        """

    def CallSeenStatusChanged(self, Call, Seen):
        """This event occurs when the seen status of a call changes.

        :Parameters:
          Call : `Call`
            Call object.
          Seen : bool
            True if call was seen.

        :see: `Call.Seen`
        """

    def CallStatus(self, Call, Status):
        """This event is caused by a change in call status.

        :Parameters:
          Call : `Call`
            Call object.
          Status : `enums`.cls*
            New status of the call.
        """

    def CallTransferStatusChanged(self, Call, Status):
        """This event occurs when a call transfer status changes.

        :Parameters:
          Call : `Call`
            Call object.
          Status : `enums`.cls*
            New status of the call transfer.
        """

    def CallVideoReceiveStatusChanged(self, Call, Status):
        """This event occurs when a call video receive status changes.

        :Parameters:
          Call : `Call`
            Call object.
          Status : `enums`.vss*
            New video receive status of the call.
        """

    def CallVideoSendStatusChanged(self, Call, Status):
        """This event occurs when a call video send status changes.

        :Parameters:
          Call : `Call`
            Call object.
          Status : `enums`.vss*
            New video send status of the call.
        """

    def CallVideoStatusChanged(self, Call, Status):
        """This event occurs when a call video status changes.

        :Parameters:
          Call : `Call`
            Call object.
          Status : `enums`.cvs*
            New video status of the call.
        """

    def ChatMemberRoleChanged(self, Member, Role):
        """This event occurs when a chat member role changes.

        :Parameters:
          Member : `ChatMember`
            Chat member object.
          Role : `enums`.chatMemberRole*
            New member role.
        """

    def ChatMembersChanged(self, Chat, Members):
        """This event occurs when a list of chat members change.

        :Parameters:
          Chat : `Chat`
            Chat object.
          Members : `UserCollection`
            Chat members.
        """

    def ChatWindowState(self, Chat, State):
        """This event occurs when chat window is opened or closed.

        :Parameters:
          Chat : `Chat`
            Chat object.
          State : bool
            True if the window was opened or False if closed.
        """

    def ClientWindowState(self, State):
        """This event occurs when the state of the client window changes.

        :Parameters:
          State : `enums`.wnd*
            New window state.
        """

    def Command(self, command):
        """This event is triggered when a command is sent to the Skype API.

        :Parameters:
          command : `Command`
            Command object.
        """

    def ConnectionStatus(self, Status):
        """This event is caused by a connection status change.

        :Parameters:
          Status : `enums`.con*
            New connection status.
        """

    def ContactsFocused(self, Username):
        """This event is caused by a change in contacts focus.

        :Parameters:
          Username : str
            Name of the user that was focused or empty string if focus was lost.
        """

    def Error(self, command, Number, Description):
        """This event is triggered when an error occurs during execution of an API command.

        :Parameters:
          command : `Command`
            Command object that caused the error.
          Number : int
            Error number returned by the Skype API.
          Description : unicode
            Description of the error.
        """

    def FileTransferStatusChanged(self, Transfer, Status):
        """This event occurs when a file transfer status changes.

        :Parameters:
          Transfer : `FileTransfer`
            File transfer object.
          Status : `enums`.fileTransferStatus*
            New status of the file transfer.
        """

    def GroupDeleted(self, GroupId):
        """This event is caused by a user deleting a custom contact group.

        :Parameters:
          GroupId : int
            Id of the deleted group.
        """

    def GroupExpanded(self, Group, Expanded):
        """This event is caused by a user expanding or collapsing a group in the contacts tab.

        :Parameters:
          Group : `Group`
            Group object.
          Expanded : bool
            Tells if the group is expanded (True) or collapsed (False).
        """

    def GroupUsers(self, Group, Count):
        """This event is caused by a change in a contact group members.

        :Parameters:
          Group : `Group`
            Group object.
          Count : int
            Number of group members.

        :note: This event is different from its Skype4COM equivalent in that the second
               parameter is number of users instead of `UserCollection` object. This
               object may be obtained using ``Group.Users`` property.
        """

    def GroupVisible(self, Group, Visible):
        """This event is caused by a user hiding/showing a group in the contacts tab.

        :Parameters:
          Group : `Group`
            Group object.
          Visible : bool
            Tells if the group is visible or not.
        """

    def MessageHistory(self, Username):
        """This event is caused by a change in message history.

        :Parameters:
          Username : str
            Name of the user whose message history changed.
        """

    def MessageStatus(self, Message, Status):
        """This event is caused by a change in chat message status.

        :Parameters:
          Message : `ChatMessage`
            Chat message object.
          Status : `enums`.cms*
            New status of the chat message.
        """

    def Mute(self, Mute):
        """This event is caused by a change in mute status.

        :Parameters:
          Mute : bool
            New mute status.
        """

    def Notify(self, Notification):
        """This event is triggered whenever Skype client sends a notification.

        :Parameters:
          Notification : unicode
            Notification string.

        :note: Use this event only if there is no dedicated one.
        """

    def OnlineStatus(self, User, Status):
        """This event is caused by a change in the online status of a user.

        :Parameters:
          User : `User`
            User object.
          Status : `enums`.ols*
            New online status of the user.
        """

    def PluginEventClicked(self, Event):
        """This event occurs when a user clicks on a plug-in event.

        :Parameters:
          Event : `PluginEvent`
            Plugin event object.
        """

    def PluginMenuItemClicked(self, MenuItem, Users, PluginContext, ContextId):
        """This event occurs when a user clicks on a plug-in menu item.

        :Parameters:
          MenuItem : `PluginMenuItem`
            Menu item object.
          Users : `UserCollection`
            Users this item refers to.
          PluginContext : unicode
            Plug-in context.
          ContextId : str or int
            Context Id. Chat name for chat context or Call ID for call context.

        :see: `PluginMenuItem`
        """

    def Reply(self, command):
        """This event is triggered when the API replies to a command object.

        :Parameters:
          command : `Command`
            Command object.
        """

    def SilentModeStatusChanged(self, Silent):
        """This event occurs when a silent mode is switched off.

        :Parameters:
          Silent : bool
            Skype client silent status.
        """

    def SmsMessageStatusChanged(self, Message, Status):
        """This event is caused by a change in the SMS message status.

        :Parameters:
          Message : `SmsMessage`
            SMS message object.
          Status : `enums`.smsMessageStatus*
            New status of the SMS message.
        """

    def SmsTargetStatusChanged(self, Target, Status):
        """This event is caused by a change in the SMS target status.

        :Parameters:
          Target : `SmsTarget`
            SMS target object.
          Status : `enums`.smsTargetStatus*
            New status of the SMS target.
        """

    def UserAuthorizationRequestReceived(self, User):
        """This event occurs when user sends you an authorization request.

        :Parameters:
          User : `User`
            User object.
        """

    def UserMood(self, User, MoodText):
        """This event is caused by a change in the mood text of the user.

        :Parameters:
          User : `User`
            User object.
          MoodText : unicode
            New mood text.
        """

    def UserStatus(self, Status):
        """This event is caused by a user status change.

        :Parameters:
          Status : `enums`.cus*
            New user status.
        """

    def VoicemailStatus(self, Mail, Status):
        """This event is caused by a change in voicemail status.

        :Parameters:
          Mail : `Voicemail`
            Voicemail object.
          Status : `enums`.vms*
            New status of the voicemail.
        """

    def WallpaperChanged(self, Path):
        """This event occurs when client wallpaper changes.

        :Parameters:
          Path : str
            Path to new wallpaper bitmap.
        """


Skype._AddEvents(SkypeEvents)
