"""Current user profile.
"""
__docformat__ = 'restructuredtext en'


import weakref

from utils import *


class Profile(object):
    """Represents the profile of currently logged in user. Access using
    `skype.Skype.CurrentUserProfile`.
    """

    def __init__(self, Skype):
        """__init__.

        :Parameters:
          Skype : `Skype`
            Skype object.
        """
        self._SkypeRef = weakref.ref(Skype)

    def _Property(self, PropName, Set=None):
        return self._Skype._Property('PROFILE', '', PropName, Set)

    def _Get_Skype(self):
        skype = self._SkypeRef()
        if skype:
            return skype
        raise Exception()

    _Skype = property(_Get_Skype)

    def _GetAbout(self):
        return self._Property('ABOUT')

    def _SetAbout(self, Value):
        self._Property('ABOUT', Value)

    About = property(_GetAbout, _SetAbout,
    doc=""""About" field of the profile.

    :type: unicode
    """)

    def _GetBalance(self):
        return int(self._Property('PSTN_BALANCE'))

    Balance = property(_GetBalance,
    doc="""Skype credit balance. Note that the precision of profile balance value is currently
    fixed at 2 decimal places, regardless of currency or any other settings. Use `BalanceValue`
    to get the balance expressed in currency.

    :type: int

    :see: `BalanceCurrency`, `BalanceToText`, `BalanceValue`
    """)

    def _GetBalanceCurrency(self):
        return self._Property('PSTN_BALANCE_CURRENCY')

    BalanceCurrency = property(_GetBalanceCurrency,
    doc="""Skype credit balance currency.

    :type: unicode

    :see: `Balance`, `BalanceToText`, `BalanceValue`
    """)

    def _GetBalanceToText(self):
        return (u'%s %.2f' % (self.BalanceCurrency, self.BalanceValue)).strip()

    BalanceToText = property(_GetBalanceToText,
    doc="""Skype credit balance as properly formatted text with currency.

    :type: unicode

    :see: `Balance`, `BalanceCurrency`, `BalanceValue`
    """)

    def _GetBalanceValue(self):
        return float(self._Property('PSTN_BALANCE')) / 100

    BalanceValue = property(_GetBalanceValue,
    doc="""Skype credit balance expressed in currency.

    :type: float

    :see: `Balance`, `BalanceCurrency`, `BalanceToText`
    """)

    def _GetBirthday(self):
        value = self._Property('BIRTHDAY')
        if len(value) == 8:
            from datetime import date
            from time import strptime
            return date(*strptime(value, '%Y%m%d')[:3])

    def _SetBirthday(self, Value):
        if Value:
            self._Property('BIRTHDAY', Value.strftime('%Y%m%d'))
        else:
            self._Property('BIRTHDAY', 0)

    Birthday = property(_GetBirthday, _SetBirthday,
    doc=""""Birthday" field of the profile.

    :type: datetime.date
    """)

    def _GetCallApplyCF(self):
        return (self._Property('CALL_APPLY_CF') == 'TRUE')

    def _SetCallApplyCF(self, Value):
        self._Property('CALL_APPLY_CF', cndexp(Value, 'TRUE', 'FALSE'))

    CallApplyCF = property(_GetCallApplyCF, _SetCallApplyCF,
    doc="""Tells if call forwarding is enabled in the profile.

    :type: bool
    """)

    def _GetCallForwardRules(self):
        return str(self._Property('CALL_FORWARD_RULES'))

    def _SetCallForwardRules(self, Value):
        self._Property('CALL_FORWARD_RULES', Value)

    CallForwardRules = property(_GetCallForwardRules, _SetCallForwardRules,
    doc="""Call forwarding rules of the profile.

    :type: str
    """)

    def _GetCallNoAnswerTimeout(self):
        return int(self._Property('CALL_NOANSWER_TIMEOUT'))

    def _SetCallNoAnswerTimeout(self, Value):
        self._Property('CALL_NOANSWER_TIMEOUT', Value)

    CallNoAnswerTimeout = property(_GetCallNoAnswerTimeout, _SetCallNoAnswerTimeout,
    doc="""Number of seconds a call will ring without being answered before it
    stops ringing.

    :type: int
    """)

    def _GetCallSendToVM(self):
        return (self._Property('CALL_SEND_TO_VM') == 'TRUE')

    def _SetCallSendToVM(self, Value):
        self._Property('CALL_SEND_TO_VM', cndexp(Value, 'TRUE', 'FALSE'))

    CallSendToVM = property(_GetCallSendToVM, _SetCallSendToVM,
    doc="""Tells whether calls will be sent to the voicemail.

    :type: bool
    """)

    def _GetCity(self):
        return self._Property('CITY')

    def _SetCity(self, Value):
        self._Property('CITY', Value)

    City = property(_GetCity, _SetCity,
    doc=""""City" field of the profile.

    :type: unicode
    """)

    def _GetCountry(self):
        return chop(self._Property('COUNTRY'))[0]

    def _SetCountry(self, Value):
        self._Property('COUNTRY', Value)

    Country = property(_GetCountry, _SetCountry,
    doc=""""Country" field of the profile.

    :type: unicode
    """)

    def _GetFullName(self):
        return self._Property('FULLNAME')

    def _SetFullName(self, Value):
        self._Property('FULLNAME', Value)

    FullName = property(_GetFullName, _SetFullName,
    doc=""""Full name" field of the profile.

    :type: unicode
    """)

    def _GetHomepage(self):
        return self._Property('HOMEPAGE')

    def _SetHomepage(self, Value):
        self._Property('HOMEPAGE', Value)

    Homepage = property(_GetHomepage, _SetHomepage,
    doc=""""Homepage" field of the profile.

    :type: unicode
    """)

    def _GetIPCountry(self):
        return str(self._Property('IPCOUNTRY'))

    IPCountry = property(_GetIPCountry,
    doc="""ISO country code queried by IP address.

    :type: str
    """)

    def _GetLanguages(self):
        return [str(x) for x in split(self._Property('LANGUAGES'))]

    def _SetLanguages(self, Value):
        self._Property('LANGUAGES', ' '.join(Value))

    Languages = property(_GetLanguages, _SetLanguages,
    doc=""""ISO language codes of the profile.

    :type: list of str
    """)

    def _GetMoodText(self):
        return self._Property('MOOD_TEXT')

    def _SetMoodText(self, Value):
        self._Property('MOOD_TEXT', Value)

    MoodText = property(_GetMoodText, _SetMoodText,
    doc=""""Mood text" field of the profile.

    :type: unicode
    """)

    def _GetPhoneHome(self):
        return self._Property('PHONE_HOME')

    def _SetPhoneHome(self, Value):
        self._Property('PHONE_HOME', Value)

    PhoneHome = property(_GetPhoneHome, _SetPhoneHome,
    doc=""""Phone home" field of the profile.

    :type: unicode
    """)

    def _GetPhoneMobile(self):
        return self._Property('PHONE_MOBILE')

    def _SetPhoneMobile(self, Value):
        self._Property('PHONE_MOBILE', Value)

    PhoneMobile = property(_GetPhoneMobile, _SetPhoneMobile,
    doc=""""Phone mobile" field of the profile.

    :type: unicode
    """)

    def _GetPhoneOffice(self):
        return self._Property('PHONE_OFFICE')

    def _SetPhoneOffice(self, Value):
        self._Property('PHONE_OFFICE', Value)

    PhoneOffice = property(_GetPhoneOffice, _SetPhoneOffice,
    doc=""""Phone office" field of the profile.

    :type: unicode
    """)

    def _GetProvince(self):
        return self._Property('PROVINCE')

    def _SetProvince(self, Value):
        self._Property('PROVINCE', Value)

    Province = property(_GetProvince, _SetProvince,
    doc=""""Province" field of the profile.

    :type: unicode
    """)

    def _GetRichMoodText(self):
        return self._Property('RICH_MOOD_TEXT')

    def _SetRichMoodText(self, Value):
        self._Property('RICH_MOOD_TEXT', Value)

    RichMoodText = property(_GetRichMoodText, _SetRichMoodText,
    doc="""Rich mood text of the profile.

    :type: unicode

    :see: https://developer.skype.com/Docs/ApiDoc/SET_PROFILE_RICH_MOOD_TEXT
    """)

    def _GetSex(self):
        return str(self._Property('SEX'))

    def _SetSex(self, Value):
        self._Property('SEX', Value)

    Sex = property(_GetSex, _SetSex,
    doc=""""Sex" field of the profile.

    :type: `enums`.usex*
    """)

    def _GetTimezone(self):
        return int(self._Property('TIMEZONE'))

    def _SetTimezone(self, Value):
        self._Property('TIMEZONE', Value)

    Timezone = property(_GetTimezone, _SetTimezone,
    doc="""Timezone of the current profile in minutes from GMT.

    :type: int
    """)

    def _GetValidatedSmsNumbers(self):
        return [str(x) for x in split(self._Property('SMS_VALIDATED_NUMBERS'), ', ')]

    ValidatedSmsNumbers = property(_GetValidatedSmsNumbers,
    doc="""List of phone numbers the user has registered for usage in reply-to
    field of SMS messages.

    :type: list of str
    """)
