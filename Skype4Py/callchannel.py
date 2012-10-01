"""Data channels for calls.
"""
__docformat__ = 'restructuredtext en'


import time
from copy import copy

from utils import *
from enums import *
from errors import SkypeError


class CallChannelManager(EventHandlingBase):
    """Instantiate this class to create a call channel manager. A call channel manager will
    automatically create a data channel (based on the APP2APP protocol) for voice calls.

    Usage
    =====

       You should access this class using the alias at the package level:
       
       .. python::

           import Skype4Py

           skype = Skype4Py.Skype()

           ccm = Skype4Py.CallChannelManager()
           ccm.Connect(skype)

       Read the constructor (`CallChannelManager.__init__`) documentation for a list of
       accepted arguments.

    Events
    ======

       This class provides events.

       The events names and their arguments lists can be found in the
       `CallChannelManagerEvents` class in this module.

       The use of events is explained in `EventHandlingBase` class which
       is a superclass of this class.
    """

    def __del__(self):
        if getattr(self, '_App', None):
            self._App.Delete()
            self._App = None
            self._Skype.UnregisterEventHandler('ApplicationStreams', self._OnApplicationStreams)
            self._Skype.UnregisterEventHandler('ApplicationReceiving', self._OnApplicationReceiving)
            self._Skype.UnregisterEventHandler('ApplicationDatagram', self._OnApplicationDatagram)

    def __init__(self, Events=None, Skype=None):
        """Initializes the object.
        
        :Parameters:
          Events
            An optional object with event handlers. See `EventHandlingBase` for more
            information on events.
        """
        EventHandlingBase.__init__(self)
        if Events:
            self._SetEventHandlerObj(Events)

        self._App = None
        self._Name = u'CallChannelManager'
        self._ChannelType = cctReliable
        self._Channels = []
        self.Connect(Skype)

    def _ApplicationDatagram(self, App, Stream, Text):
        if App == self._App:
            for ch in self_Channels:
                if ch['stream'] == Stream:
                    msg = CallChannelMessage(Text)
                    self._CallEventHandler('Message', self, CallChannel(self, ch), msg)
                    break

    def _ApplicationReceiving(self, App, Streams):
        if App == self._App:
            for ch in self._Channels:
                if ch['stream'] in Streams:
                    msg = CallChannelMessage(ch.Stream.Read())
                    self._CallEventHandler('Message', self, CallChannel(self, ch), msg)

    def _ApplicationStreams(self, App, Streams):
        if App == self._App:
            for ch in self._Channels:
                if ch['stream'] not in Streams:
                    self._Channels.remove(ch)
                    self._CallEventHandler('Channels', self, self.Channels)

    def _CallStatus(self, Call, Status):
        if Status == clsRinging:
            if self._App is None:
                self.CreateApplication()
            self._App.Connect(Call.PartnerHandle, True)
            for stream in self._App.Streams:
                if stream.PartnerHandle == Call.PartnerHandle:
                    self._Channels.append(dict(call=Call, stream=stream))
                    self._CallEventHandler('Channels', self, self.Channels)
                    break
        elif Status in (clsCancelled, clsFailed, clsFinished, clsRefused, clsMissed):
            for ch in self._Channels:
                if ch['call'] == Call:
                    self._Channels.remove(ch)
                    self._CallEventHandler('Channels', self, self.Channels)
                    try:
                        ch['stream'].Disconnect()
                    except SkypeError:
                        pass
                    break

    def Connect(self, Skype):
        """Connects this call channel manager instance to Skype. This is the first thing you should
        do after creating this object.

        :Parameters:
          Skype : `Skype`
            The Skype object.

        :see: `Disconnect`
        """
        self._Skype = Skype
        self._Skype.RegisterEventHandler('CallStatus', self._CallStatus)
        del self._Channels[:]

    def CreateApplication(self, ApplicationName=None):
        """Creates an APP2APP application context. The application is automatically created using
        `application.Application.Create` method.
        
        :Parameters:
          ApplicationName : unicode
            Application name. Initial name, when the manager is created, is ``u'CallChannelManager'``.
        """
        if ApplicationName is not None:
            self.Name = tounicode(ApplicationName)
        self._App = self._Skype.Application(self.Name)
        self._Skype.RegisterEventHandler('ApplicationStreams', self._ApplicationStreams)
        self._Skype.RegisterEventHandler('ApplicationReceiving', self._ApplicationReceiving)
        self._Skype.RegisterEventHandler('ApplicationDatagram', self._ApplicationDatagram)
        self._App.Create()
        self._CallEventHandler('Created', self)

    def Disconnect(self):
        """Disconnects from the Skype instance.
        
        :see: `Connect`
        """
        self._Skype.UnregisterEventHandler('CallStatus', self._CallStatus)
        self._Skype = None

    def _GetChannels(self):
        return tuple(self._Channels)

    Channels = property(_GetChannels,
    doc="""All call data channels.

    :type: tuple of `CallChannel`
    """)

    def _GetChannelType(self):
        return self._ChannelType

    def _SetChannelType(self, Value):
        self._ChannelType = str(Value)

    ChannelType = property(_GetChannelType, _SetChannelType,
    doc="""Queries/sets the default channel type.

    :type: `enums`.cct*
    """)

    def _GetCreated(self):
        return (not not self._App)

    Created = property(_GetCreated,
    doc="""Returns True if the application context has been created.

    :type: bool
    """)

    def _GetName(self):
        return self._Name

    def _SetName(self, Value):
        self._Name = tounicode(Value)

    Name = property(_GetName, _SetName,
    doc="""Queries/sets the application context name.

    :type: unicode
    """)


class CallChannelManagerEvents(object):
    """Events defined in `CallChannelManager`.

    See `EventHandlingBase` for more information on events.
    """

    def Channels(self, Manager, Channels):
        """This event is triggered when list of call channels changes.

        :Parameters:
          Manager : `CallChannelManager`
            The call channel manager object.
          Channels : tuple of `CallChannel`
            Updated list of call channels.
        """

    def Created(self, Manager):
        """This event is triggered when the application context has successfully been created.

        :Parameters:
          Manager : `CallChannelManager`
            The call channel manager object.
        """

    def Message(self, Manager, Channel, Message):
        """This event is triggered when a call channel message has been received.

        :Parameters:
          Manager : `CallChannelManager`
            The call channel manager object.
          Channel : `CallChannel`
            The call channel object receiving the message.
          Message : `CallChannelMessage`
            The received message.
        """


CallChannelManager._AddEvents(CallChannelManagerEvents)


class CallChannel(object):
    """Represents a call channel.
    """

    def __repr__(self):
        return Cached.__repr__(self, 'Manager', 'Call', 'Stream')

    def SendTextMessage(self, Text):
        """Sends a text message over channel.

        :Parameters:
          Text : unicode
            Text to send.
        """
        if self.Type == cctReliable:
            self.Stream.Write(Text)
        elif self.Type == cctDatagram:
            self.Stream.SendDatagram(Text)
        else:
            raise SkypeError(0, 'Cannot send using %s channel type' & repr(self.Type))

    def _GetCall(self):
        return self._Handle['call']

    Call = property(_GetCall,
    doc="""The call object associated with this channel.

    :type: `Call`
    """)

    def _GetManager(self):
        return self._Owner

    Manager = property(_GetManager,
    doc="""The call channel manager object.

    :type: `CallChannelManager`
    """)

    def _GetStream(self):
        return self._Handle['stream']

    Stream = property(_GetStream,
    doc="""Underlying APP2APP stream object.

    :type: `ApplicationStream`
    """)

    def _GetType(self):
        return self._Handle.get('type', self.Manager.ChannelType)

    def _SetType(self, Value):
        self._Handle['type'] = str(Value)

    Type = property(_GetType, _SetType,
    doc="""Type of this channel.

    :type: `enums`.cct*
    """)


class CallChannelMessage(object):
    """Represents a call channel message.
    """

    def __init__(self, Text):
        """Initializes the object.

        :Parameters:
          Text : unicode
            The message text.
        """
        self._Text = tounicode(Text)

    def _GetText(self):
        return self._Text

    def _SetText(self, Value):
        self._Text = tounicode(Value)

    Text = property(_GetText, _SetText,
    doc="""Queries/sets the message text.

    :type: unicode
    """)
