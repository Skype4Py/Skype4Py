"""APP2APP protocol.
"""
__docformat__ = 'restructuredtext en'


import threading

from utils import *
from user import *


class Application(Cached):
    """Represents an application in APP2APP protocol. Use `skype.Skype.Application` to instantiate.
    """
    _ValidateHandle = staticmethod(tounicode)

    def __repr__(self):
        return Cached.__repr__(self, 'Name')

    def _Alter(self, AlterName, Args=None):
        return self._Owner._Alter('APPLICATION', self.Name, AlterName, Args)

    def _Init(self):
        self._MakeOwner()

    def _Property(self, PropName, Set=None):
        return self._Owner._Property('APPLICATION', self.Name, PropName, Set)

    def _Connect_ApplicationStreams(self, App, Streams):
        if App == self:
            s = [x for x in Streams if x.PartnerHandle == self._Connect_Username]
            if s:
                self._Connect_Stream[0] = s[0]
                self._Connect_Event.set()

    def Connect(self, Username, WaitConnected=False):
        """Connects application to user.

        :Parameters:
          Username : str
            Name of the user to connect to.
          WaitConnected : bool
            If True, causes the method to wait until the connection is established.

        :return: If ``WaitConnected`` is True, returns the stream which can be used to send the
                 data. Otherwise returns None.
        :rtype: `ApplicationStream` or None
        """
        if WaitConnected:
            self._Connect_Event = threading.Event()
            self._Connect_Stream = [None]
            self._Connect_Username = Username
            self._Connect_ApplicationStreams(self, self.Streams)
            self._Owner.RegisterEventHandler('ApplicationStreams', self._Connect_ApplicationStreams)
            self._Alter('CONNECT', Username)
            self._Connect_Event.wait()
            self._Owner.UnregisterEventHandler('ApplicationStreams', self._Connect_ApplicationStreams)
            try:
                return self._Connect_Stream[0]
            finally:
                del self._Connect_Stream, self._Connect_Event, self._Connect_Username
        else:
            self._Alter('CONNECT', Username)

    def Create(self):
        """Creates the APP2APP application in Skype client.
        """
        self._Owner._DoCommand('CREATE APPLICATION %s' % self.Name)

    def Delete(self):
        """Deletes the APP2APP application in Skype client.
        """
        self._Owner._DoCommand('DELETE APPLICATION %s' % self.Name)

    def SendDatagram(self, Text, Streams=None):
        """Sends datagram to application streams.

        :Parameters:
          Text : unicode
            Text to send.
          Streams : sequence of `ApplicationStream`
            Streams to send the datagram to or None if all currently connected streams should be
            used.
        """
        if Streams is None:
            Streams = self.Streams
        for s in Streams:
            s.SendDatagram(Text)

    def _GetConnectableUsers(self):
        return UserCollection(self._Owner, split(self._Property('CONNECTABLE')))

    ConnectableUsers = property(_GetConnectableUsers,
    doc="""All connectible users.

    :type: `UserCollection`
    """)

    def _GetConnectingUsers(self):
        return UserCollection(self._Owner, split(self._Property('CONNECTING')))

    ConnectingUsers = property(_GetConnectingUsers,
    doc="""All users connecting at the moment.

    :type: `UserCollection`
    """)

    def _GetName(self):
        return self._Handle

    Name = property(_GetName,
    doc="""Name of the application.

    :type: unicode
    """)

    def _GetReceivedStreams(self):
        return ApplicationStreamCollection(self, (x.split('=')[0] for x in split(self._Property('RECEIVED'))))

    ReceivedStreams = property(_GetReceivedStreams,
    doc="""All streams that received data and can be read.

    :type: `ApplicationStreamCollection`
    """)

    def _GetSendingStreams(self):
        return ApplicationStreamCollection(self, (x.split('=')[0] for x in split(self._Property('SENDING'))))

    SendingStreams = property(_GetSendingStreams,
    doc="""All streams that send data and at the moment.

    :type: `ApplicationStreamCollection`
    """)

    def _GetStreams(self):
        return ApplicationStreamCollection(self, split(self._Property('STREAMS')))

    Streams = property(_GetStreams,
    doc="""All currently connected application streams.

    :type: `ApplicationStreamCollection`
    """)


class ApplicationStream(Cached):
    """Represents an application stream in APP2APP protocol.
    """
    _ValidateHandle = str

    def __len__(self):
        return self.DataLength

    def __repr__(self):
        return Cached.__repr__(self, 'Handle')

    def Disconnect(self):
        """Disconnects the stream.
        """
        self.Application._Alter('DISCONNECT', self.Handle)

    close = Disconnect

    def Read(self):
        """Reads data from stream.

        :return: Read data or an empty string if none were available.
        :rtype: unicode
        """
        return self.Application._Alter('READ', self.Handle)

    read = Read

    def SendDatagram(self, Text):
        """Sends datagram to stream.

        :Parameters:
          Text : unicode
            Datagram to send.
        """
        self.Application._Alter('DATAGRAM', '%s %s' % (self.Handle, tounicode(Text)))

    def Write(self, Text):
        """Writes data to stream.

        :Parameters:
          Text : unicode
            Data to send.
        """
        self.Application._Alter('WRITE', '%s %s' % (self.Handle, tounicode(Text)))

    write = Write

    def _GetApplication(self):
        return self._Owner

    Application = property(_GetApplication,
    doc="""Application this stream belongs to.

    :type: `Application`
    """)

    def _GetApplicationName(self):
        return self.Application.Name

    ApplicationName = property(_GetApplicationName,
    doc="""Name of the application this stream belongs to. Same as ``ApplicationStream.Application.Name``.

    :type: unicode
    """)

    def _GetDataLength_GetStreamLength(self, Type):
        for s in split(self.Application._Property(Type)):
            h, i = s.split('=')
            if h == self.Handle:
                return int(i)

    def _GetDataLength(self):
        i = self._GetDataLength_GetStreamLength('SENDING')
        if i is not None:
            return i
        i = self._GetDataLength_GetStreamLength('RECEIVED')
        if i is not None:
            return i
        return 0

    DataLength = property(_GetDataLength,
    doc="""Number of bytes awaiting in the read buffer.

    :type: int
    """)

    def _GetHandle(self):
        return self._Handle

    Handle = property(_GetHandle,
    doc="""Stream handle in u'<Skypename>:<n>' format.

    :type: str
    """)

    def _GetPartnerHandle(self):
        return self.Handle.split(':')[0]

    PartnerHandle = property(_GetPartnerHandle,
    doc="""Skypename of the user this stream is connected to.

    :type: str
    """)


class ApplicationStreamCollection(CachedCollection):
    _CachedType = ApplicationStream
