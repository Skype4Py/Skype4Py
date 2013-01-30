"""Voicemails.
"""
__docformat__ = 'restructuredtext en'


from utils import *
from enums import *
from call import DeviceMixin


class Voicemail(Cached, DeviceMixin):
    """Represents a voicemail.
    """
    _ValidateHandle = int

    def __repr__(self):
        return Cached.__repr__(self, 'Id')

    def _Alter(self, AlterName, Args=None):
        return self._Owner._Alter('VOICEMAIL', self.Id, AlterName, Args)

    def _Property(self, PropName, Set=None, Cache=True):
        return self._Owner._Property('VOICEMAIL', self.Id, PropName, Set, Cache)

    def Delete(self):
        """Deletes this voicemail.
        """
        self._Alter('DELETE')

    def Download(self):
        """Downloads this voicemail object from the voicemail server to a local computer.
        """
        self._Alter('DOWNLOAD')

    def Open(self):
        """Opens and plays this voicemail.
        """
        self._Owner._DoCommand('OPEN VOICEMAIL %s' % self.Id)

    def SetUnplayed(self):
        """Changes the status of a voicemail from played to unplayed.
        """
        # Note. Due to a bug in Skype (tested using 3.8.0.115) the reply from
        # [ALTER VOICEMAIL <id> SETUNPLAYED] is [ALTER VOICEMAIL <id> DELETE]
        # causing the _Alter method to fail. Therefore we have to use a direct
        # _DoCommand instead. For the event of this being fixed, we don't
        # check for the "SETUNPLAYED"/"DELETE" part of the response.
        
        #self._Alter('SETUNPLAYED')
        self._Owner._DoCommand('ALTER VOICEMAIL %d SETUNPLAYED' % self.Id,
                               'ALTER VOICEMAIL %d' % self.Id)

    def StartPlayback(self):
        """Starts playing downloaded voicemail.
        """
        self._Alter('STARTPLAYBACK')

    def StartPlaybackInCall(self):
        """Starts playing downloaded voicemail during a call.
        """
        self._Alter('STARTPLAYBACKINCALL')

    def StartRecording(self):
        """Stops playing a voicemail greeting and starts recording a voicemail message.
        """
        self._Alter('STARTRECORDING')

    def StopPlayback(self):
        """Stops playing downloaded voicemail.
        """
        self._Alter('STOPPLAYBACK')

    def StopRecording(self):
        """Ends the recording of a voicemail message.
        """
        self._Alter('STOPRECORDING')

    def Upload(self):
        """Uploads recorded voicemail from a local computer to the voicemail server.
        """
        self._Alter('UPLOAD')

    def _GetAllowedDuration(self):
        return int(self._Property('ALLOWED_DURATION'))

    AllowedDuration = property(_GetAllowedDuration,
    doc="""Maximum voicemail duration in seconds allowed to leave to partner

    :type: int
    """)

    def _GetDatetime(self):
        from datetime import datetime
        return datetime.fromtimestamp(self.Timestamp)

    Datetime = property(_GetDatetime,
    doc="""Timestamp of this voicemail expressed using datetime.

    :type: datetime.datetime
    """)

    def _GetDuration(self):
        return int(self._Property('DURATION'))

    Duration = property(_GetDuration,
    doc="""Actual voicemail duration in seconds.

    :type: int
    """)

    def _GetFailureReason(self):
        return str(self._Property('FAILUREREASON'))

    FailureReason = property(_GetFailureReason,
    doc="""Voicemail failure reason. Read if `Status` == `enums.vmsFailed`.

    :type: `enums`.vmr*
    """)

    def _GetId(self):
        return self._Handle

    Id = property(_GetId,
    doc="""Unique voicemail Id.

    :type: int
    """)

    def _GetPartnerDisplayName(self):
        return self._Property('PARTNER_DISPNAME')

    PartnerDisplayName = property(_GetPartnerDisplayName,
    doc="""DisplayName for voicemail sender (for incoming) or recipient (for outgoing).

    :type: unicode
    """)

    def _GetPartnerHandle(self):
        return str(self._Property('PARTNER_HANDLE'))

    PartnerHandle = property(_GetPartnerHandle,
    doc="""Skypename for voicemail sender (for incoming) or recipient (for outgoing).

    :type: str
    """)

    def _GetStatus(self):
        return str(self._Property('STATUS'))

    Status = property(_GetStatus,
    doc="""Voicemail status.

    :type: `enums`.vms*
    """)

    def _GetTimestamp(self):
        return float(self._Property('TIMESTAMP'))

    Timestamp = property(_GetTimestamp,
    doc="""Timestamp of this voicemail.

    :type: float
    """)

    def _GetType(self):
        return str(self._Property('TYPE'))

    Type = property(_GetType,
    doc="""Voicemail type.

    :type: `enums`.vmt*
    """)


class VoicemailCollection(CachedCollection):
    _CachedType = Voicemail
