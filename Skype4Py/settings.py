"""Skype client settings.
"""
__docformat__ = 'restructuredtext en'


import sys
import weakref

from utils import *


class Settings(object):
    """Represents Skype settings. Access using `skype.Skype.Settings`.
    """

    def __init__(self, Skype):
        """__init__.

        :Parameters:
          Skype : `Skype`
            Skype
        """
        self._SkypeRef = weakref.ref(Skype)

    def Avatar(self, Id=1, Set=None):
        """Sets user avatar picture from file.

        :Parameters:
          Id : int
            Optional avatar Id.
          Set : str
            New avatar file name.

        :deprecated: Use `LoadAvatarFromFile` instead.
        """
        from warnings import warn
        warn('Settings.Avatar: Use Settings.LoadAvatarFromFile instead.', DeprecationWarning, stacklevel=2)
        if Set is None:
            raise TypeError('Argument \'Set\' is mandatory!')
        self.LoadAvatarFromFile(Set, Id)

    def LoadAvatarFromFile(self, Filename, AvatarId=1):
        """Loads user avatar picture from file.

        :Parameters:
          Filename : str
            Name of the avatar file.
          AvatarId : int
            Optional avatar Id.
        """
        s = 'AVATAR %s %s' % (AvatarId, path2unicode(Filename))
        self._Skype._DoCommand('SET %s' % s, s)

    def ResetIdleTimer(self):
        """Reset Skype idle timer.
        """
        self._Skype._DoCommand('RESETIDLETIMER')

    def RingTone(self, Id=1, Set=None):
        """Returns/sets a ringtone.

        :Parameters:
          Id : int
            Ringtone Id
          Set : str
            Path to new ringtone or None if the current path should be queried.

        :return: Current path if Set=None, None otherwise.
        :rtype: str or None
        """
        if Set is None:
            return unicode2path(self._Skype._Property('RINGTONE', Id, ''))
        self._Skype._Property('RINGTONE', Id, '', path2unicode(Set))

    def RingToneStatus(self, Id=1, Set=None):
        """Enables/disables a ringtone.

        :Parameters:
          Id : int
            Ringtone Id
          Set : bool
            True/False if the ringtone should be enabled/disabled or None if the current status
            should be queried.

        :return: Current status if Set=None, None otherwise.
        :rtype: bool
        """
        if Set is None:
            return (self._Skype._Property('RINGTONE', Id, 'STATUS') == 'ON')
        self._Skype._Property('RINGTONE', Id, 'STATUS', cndexp(Set, 'ON', 'OFF'))

    def SaveAvatarToFile(self, Filename, AvatarId=1):
        """Saves user avatar picture to file.

        :Parameters:
          Filename : str
            Destination path.
          AvatarId : int
            Avatar Id
        """
        s = 'AVATAR %s %s' % (AvatarId, path2unicode(Filename))
        self._Skype._DoCommand('GET %s' % s, s)

    def _Get_Skype(self):
        skype = self._SkypeRef()
        if skype:
            return skype
        raise ISkypeError('Skype4Py internal error')

    _Skype = property(_Get_Skype)

    def _GetAEC(self):
        return (self._Skype.Variable('AEC') == 'ON')

    def _SetAEC(self, Value):
        self._Skype.Variable('AEC', cndexp(Value, 'ON', 'OFF'))

    AEC = property(_GetAEC, _SetAEC,
    doc="""Automatic echo cancellation state.

    :type: bool

    :warning: Starting with Skype for Windows 3.6, this property has no effect. It can still be set
              for backwards compatibility reasons.
    """)

    def _GetAGC(self):
        return (self._Skype.Variable('AGC') == 'ON')

    def _SetAGC(self, Value):
        self._Skype.Variable('AGC', cndexp(Value, 'ON', 'OFF'))

    AGC = property(_GetAGC, _SetAGC,
    doc="""Automatic gain control state.

    :type: bool

    :warning: Starting with Skype for Windows 3.6, this property has no effect. It can still be set
              for backwards compatibility reasons.
    """)

    def _GetAudioIn(self):
        return self._Skype.Variable('AUDIO_IN')

    def _SetAudioIn(self, Value):
        self._Skype.Variable('AUDIO_IN', Value)

    AudioIn = property(_GetAudioIn, _SetAudioIn,
    doc="""Name of an audio input device.

    :type: unicode
    """)

    def _GetAudioOut(self):
        return self._Skype.Variable('AUDIO_OUT')

    def _SetAudioOut(self, Value):
        self._Skype.Variable('AUDIO_OUT', Value)

    AudioOut = property(_GetAudioOut, _SetAudioOut,
    doc="""Name of an audio output device.

    :type: unicode
    """)

    def _GetAutoAway(self):
        return (self._Skype.Variable('AUTOAWAY') == 'ON')

    def _SetAutoAway(self, Value):
        self._Skype.Variable('AUTOAWAY', cndexp(Value, 'ON', 'OFF'))

    AutoAway = property(_GetAutoAway, _SetAutoAway,
    doc="""Auto away status.

    :type: bool
    """)

    def _GetLanguage(self):
        return str(self._Skype.Variable('UI_LANGUAGE'))

    def _SetLanguage(self, Value):
        self._Skype.Variable('UI_LANGUAGE', Value)

    Language = property(_GetLanguage, _SetLanguage,
    doc="""Language of the Skype client as an ISO code.

    :type: str
    """)

    def _GetPCSpeaker(self):
        return (self._Skype.Variable('PCSPEAKER') == 'ON')

    def _SetPCSpeaker(self, Value):
        self._Skype.Variable('PCSPEAKER', cndexp(Value, 'ON', 'OFF'))

    PCSpeaker = property(_GetPCSpeaker, _SetPCSpeaker,
    doc="""PCSpeaker status.

    :type: bool
    """)

    def _GetRinger(self):
        return self._Skype.Variable('RINGER')

    def _SetRinger(self, Value):
        self._Skype.Variable('RINGER', Value)

    Ringer = property(_GetRinger, _SetRinger,
    doc="""Name of a ringer device.

    :type: unicode
    """)

    def _GetVideoIn(self):
        return self._Skype.Variable('VIDEO_IN')

    def _SetVideoIn(self, Value):
        self._Skype.Variable('VIDEO_IN', Value)

    VideoIn = property(_GetVideoIn, _SetVideoIn,
    doc="""Name of a video input device.

    :type: unicode
    """)
