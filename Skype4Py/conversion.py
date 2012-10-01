"""Conversion between constants and text.
"""
__docformat__ = 'restructuredtext en'


import os

import enums


# Following code is needed when building executable files using py2exe.
# Together with the lang.__init__ it makes sure that all languages
# are included in the package built by py2exe. The tool looks just at
# the imports, it ignores the 'if' statement.
#
# More about py2exe: http://www.py2exe.org/

if False:
    import lang
    

class Conversion(object):
    """Allows conversion between constants and text. Access using `skype.Skype.Convert`.
    """

    def __init__(self, Skype):
        """__init__.

        :Parameters:
          Skype : `Skype`
            Skype object.
        """
        self._Language = ''
        self._Module = None
        self._SetLanguage('en')

    def _TextTo(self, Prefix, Value):
        enum = [z for z in [(y, getattr(enums, y)) for y in [x for x in dir(enums) if x.startswith(Prefix)]] if z[1] == Value]
        if enum:
            return str(Value)
        raise ValueError('Bad text')

    def _ToText(self, Prefix, Value):
        enum = [z for z in [(y, getattr(enums, y)) for y in [x for x in dir(enums) if x.startswith(Prefix)]] if z[1] == Value]
        if enum:
            try:
                return unicode(getattr(self._Module, enum[0][0]))
            except AttributeError:
                pass
        raise ValueError('Bad identifier')

    def AttachmentStatusToText(self, Status):
        """Returns attachment status as text.

        :Parameters:
          Status : `enums`.apiAttach*
            Attachment status.

        :return: Text describing the attachment status.
        :rtype: unicode
        """
        return self._ToText('api', Status)

    def BuddyStatusToText(self, Status):
        """Returns buddy status as text.

        :Parameters:
          Status : `enums`.bud*
            Buddy status.

        :return: Text describing the buddy status.
        :rtype: unicode
        """
        return self._ToText('bud', Status)

    def CallFailureReasonToText(self, Reason):
        """Returns failure reason as text.

        :Parameters:
          Reason : `enums`.cfr*
            Call failure reason.

        :return: Text describing the call failure reason.
        :rtype: unicode
        """
        return self._ToText('cfr', Reason)

    def CallStatusToText(self, Status):
        """Returns call status as text.

        :Parameters:
          Status : `enums`.cls*
            Call status.

        :return: Text describing the call status.
        :rtype: unicode
        """
        return self._ToText('cls', Status)

    def CallTypeToText(self, Type):
        """Returns call type as text.

        :Parameters:
          Type : `enums`.clt*
            Call type.

        :return: Text describing the call type.
        :rtype: unicode
        """
        return self._ToText('clt', Type)

    def CallVideoSendStatusToText(self, Status):
        """Returns call video send status as text.

        :Parameters:
          Status : `enums`.vss*
            Call video send status.

        :return: Text describing the call video send status.
        :rtype: unicode
        """
        return self._ToText('vss', Status)

    def CallVideoStatusToText(self, Status):
        """Returns call video status as text.

        :Parameters:
          Status : `enums`.cvs*
            Call video status.

        :return: Text describing the call video status.
        :rtype: unicode
        """
        return self._ToText('cvs', Status)

    def ChatLeaveReasonToText(self, Reason):
        """Returns leave reason as text.

        :Parameters:
          Reason : `enums`.lea*
            Chat leave reason.

        :return: Text describing the chat leave reason.
        :rtype: unicode
        """
        return self._ToText('lea', Reason)

    def ChatMessageStatusToText(self, Status):
        """Returns message status as text.

        :Parameters:
          Status : `enums`.cms*
            Chat message status.

        :return: Text describing the chat message status.
        :rtype: unicode
        """
        return self._ToText('cms', Status)

    def ChatMessageTypeToText(self, Type):
        """Returns message type as text.

        :Parameters:
          Type : `enums`.cme*
            Chat message type.

        :return: Text describing the chat message type.
        :rtype: unicode
        """
        return self._ToText('cme', Type)

    def ChatStatusToText(self, Status):
        """Returns chatr status as text.

        :Parameters:
          Status : `enums`.chs*
            Chat status.

        :return: Text describing the chat status.
        :rtype: unicode
        """
        return self._ToText('chs', Status)

    def ConnectionStatusToText(self, Status):
        """Returns connection status as text.

        :Parameters:
          Status : `enums`.con*
            Connection status.

        :return: Text describing the connection status.
        :rtype: unicode
        """
        return self._ToText('con', Status)

    def GroupTypeToText(self, Type):
        """Returns group type as text.

        :Parameters:
          Type : `enums`.grp*
            Group type.

        :return: Text describing the group type.
        :rtype: unicode
        """
        return self._ToText('grp', Type)

    def OnlineStatusToText(self, Status):
        """Returns online status as text.

        :Parameters:
          Status : `enums`.ols*
            Online status.

        :return: Text describing the online status.
        :rtype: unicode
        """
        return self._ToText('ols', Status)

    def SmsMessageStatusToText(self, Status):
        """Returns SMS message status as text.

        :Parameters:
          Status : `enums`.smsMessageStatus*
            SMS message status.

        :return: Text describing the SMS message status.
        :rtype: unicode
        """
        return self._ToText('smsMessageStatus', Status)

    def SmsMessageTypeToText(self, Type):
        """Returns SMS message type as text.

        :Parameters:
          Type : `enums`.smsMessageType*
            SMS message type.

        :return: Text describing the SMS message type.
        :rtype: unicode
        """
        return self._ToText('smsMessageType', Type)

    def SmsTargetStatusToText(self, Status):
        """Returns SMS target status as text.

        :Parameters:
          Status : `enums`.smsTargetStatus*
            SMS target status.

        :return: Text describing the SMS target status.
        :rtype: unicode
        """
        return self._ToText('smsTargetStatus', Status)

    def TextToAttachmentStatus(self, Text):
        """Returns attachment status code.

        :Parameters:
          Text : unicode
            Text, one of 'UNKNOWN', 'SUCCESS', 'PENDING_AUTHORIZATION', 'REFUSED', 'NOT_AVAILABLE',
            'AVAILABLE'.

        :return: Attachment status.
        :rtype: `enums`.apiAttach*
        """
        conv = {'UNKNOWN': enums.apiAttachUnknown,
                'SUCCESS': enums.apiAttachSuccess,
                'PENDING_AUTHORIZATION': enums.apiAttachPendingAuthorization,
                'REFUSED': enums.apiAttachRefused,
                'NOT_AVAILABLE': enums.apiAttachNotAvailable,
                'AVAILABLE': enums.apiAttachAvailable}
        try:
            return self._TextTo('api', conv[Text.upper()])
        except KeyError:
            raise ValueError('Bad text')

    def TextToBuddyStatus(self, Text):
        """Returns buddy status code.

        :Parameters:
          Text : unicode
            Text, one of 'UNKNOWN', 'NEVER_BEEN_FRIEND', 'DELETED_FRIEND', 'PENDING_AUTHORIZATION',
            'FRIEND'.

        :return: Buddy status.
        :rtype: `enums`.bud*
        """
        conv = {'UNKNOWN': enums.budUnknown,
                'NEVER_BEEN_FRIEND': enums.budNeverBeenFriend,
                'DELETED_FRIEND': enums.budDeletedFriend,
                'PENDING_AUTHORIZATION': enums.budPendingAuthorization,
                'FRIEND': enums.budFriend}
        try:
            return self._TextTo('bud', conv[Text.upper()])
        except KeyError:
            raise ValueError('Bad text')

    def TextToCallStatus(self, Text):
        """Returns call status code.

        :Parameters:
          Text : unicode
            Text, one of `enums`.cls*.

        :return: Call status.
        :rtype: `enums`.cls*

        :note: Currently, this method only checks if the given string is one of the allowed ones and
               returns it or raises a ``ValueError``.
        """
        return self._TextTo('cls', Text)

    def TextToCallType(self, Text):
        """Returns call type code.

        :Parameters:
          Text : unicode
            Text, one of `enums`.clt*.

        :return: Call type.
        :rtype: `enums`.clt*

        :note: Currently, this method only checks if the given string is one of the allowed ones and
               returns it or raises a ``ValueError``.
        """
        return self._TextTo('clt', Text)

    def TextToChatMessageStatus(self, Text):
        """Returns message status code.

        :Parameters:
          Text : unicode
            Text, one of `enums`.cms*.

        :return: Chat message status.
        :rtype: `enums`.cms*

        :note: Currently, this method only checks if the given string is one of the allowed ones and
               returns it or raises a ``ValueError``.
        """
        return self._TextTo('cms', Text)

    def TextToChatMessageType(self, Text):
        """Returns message type code.

        :Parameters:
          Text : unicode
            Text, one of `enums`.cme*.

        :return: Chat message type.
        :rtype: `enums`.cme*

        :note: Currently, this method only checks if the given string is one of the allowed ones and
               returns it or raises a ``ValueError``.
        """
        return self._TextTo('cme', Text)

    def TextToConnectionStatus(self, Text):
        """Retunes connection status code.

        :Parameters:
          Text : unicode
            Text, one of `enums`.con*.

        :return: Connection status.
        :rtype: `enums`.con*

        :note: Currently, this method only checks if the given string is one of the allowed ones and
               returns it or raises a ``ValueError``.
        """
        return self._TextTo('con', Text)

    def TextToGroupType(self, Text):
        """Returns group type code.

        :Parameters:
          Text : unicode
            Text, one of `enums`.grp*.

        :return: Group type.
        :rtype: `enums`.grp*

        :note: Currently, this method only checks if the given string is one of the allowed ones and
               returns it or raises a ``ValueError``.
        """
        return self._TextTo('grp', Text)

    def TextToOnlineStatus(self, Text):
        """Returns online status code.

        :Parameters:
          Text : unicode
            Text, one of `enums`.ols*.

        :return: Online status.
        :rtype: `enums`.ols*

        :note: Currently, this method only checks if the given string is one of the allowed ones and
               returns it or raises a ``ValueError``.
        """
        return self._TextTo('ols', Text)

    def TextToUserSex(self, Text):
        """Returns user sex code.

        :Parameters:
          Text : unicode
            Text, one of `enums`.usex*.

        :return: User sex.
        :rtype: `enums`.usex*

        :note: Currently, this method only checks if the given string is one of the allowed ones and
               returns it or raises a ``ValueError``.
        """
        return self._TextTo('usex', Text)

    def TextToUserStatus(self, Text):
        """Returns user status code.

        :Parameters:
          Text : unicode
            Text, one of `enums`.cus*.

        :return: User status.
        :rtype: `enums`.cus*

        :note: Currently, this method only checks if the given string is one of the allowed ones and
               returns it or raises a ``ValueError``.
        """
        return self._TextTo('cus', Text)

    def TextToVoicemailStatus(self, Text):
        """Returns voicemail status code.

        :Parameters:
          Text : unicode
            Text, one of `enums`.vms*.

        :return: Voicemail status.
        :rtype: `enums`.vms*

        :note: Currently, this method only checks if the given string is one of the allowed ones and
               returns it or raises a ``ValueError``.
        """
        return self._TextTo('vms', Text)

    def UserSexToText(self, Sex):
        """Returns user sex as text.

        :Parameters:
          Sex : `enums`.usex*
            User sex.

        :return: Text describing the user sex.
        :rtype: unicode
        """
        return self._ToText('usex', Sex)

    def UserStatusToText(self, Status):
        """Returns user status as text.

        :Parameters:
          Status : `enums`.cus*
            User status.

        :return: Text describing the user status.
        :rtype: unicode
        """
        return self._ToText('cus', Status)

    def VoicemailFailureReasonToText(self, Reason):
        """Returns voicemail failure reason as text.

        :Parameters:
          Reason : `enums`.vmr*
            Voicemail failure reason.

        :return: Text describing the voicemail failure reason.
        :rtype: unicode
        """
        return self._ToText('vmr', Reason)

    def VoicemailStatusToText(self, Status):
        """Returns voicemail status as text.

        :Parameters:
          Status : `enums`.vms*
            Voicemail status.

        :return: Text describing the voicemail status.
        :rtype: unicode
        """
        return self._ToText('vms', Status)

    def VoicemailTypeToText(self, Type):
        """Returns voicemail type as text.

        :Parameters:
          Type : `enums`.vmt*
            Voicemail type.

        :return: Text describing the voicemail type.
        :rtype: unicode
        """
        return self._ToText('vmt', Type)

    def _GetLanguage(self):
        return self._Language

    def _SetLanguage(self, Language):
        try:
            self._Module = __import__('lang.%s' % Language, globals(), locals(), ['lang'])
            self._Language = str(Language)
        except ImportError:
            raise ValueError('Unknown language: %s' % Language)

    Language = property(_GetLanguage, _SetLanguage,
    doc="""Language used for all "ToText" conversions.

    Currently supported languages: ar, bg, cs, cz, da, de, el, en, es, et, fi, fr, he, hu, it, ja, ko,
    lt, lv, nl, no, pl, pp, pt, ro, ru, sv, tr, x1.

    :type: str
    """)
