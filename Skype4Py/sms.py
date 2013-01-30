"""Short messaging system.
"""
__docformat__ = 'restructuredtext en'


from utils import *


class SmsMessage(Cached):
    """Represents an SMS message.
    """
    _ValidateHandle = int

    def __repr__(self):
        return Cached.__repr__(self, 'Id')

    def _Alter(self, AlterName, Args=None):
        return self._Owner._Alter('SMS', self.Id, AlterName, Args)

    def _Init(self):
        self._MakeOwner()

    def _Property(self, PropName, Set=None, Cache=True):
        return self._Owner._Property('SMS', self.Id, PropName, Set, Cache)

    def Delete(self):
        """Deletes this SMS message.
        """
        self._Owner._DoCommand('DELETE SMS %s' % self.Id)

    def MarkAsSeen(self):
        """Marks this SMS message as seen.
        """
        self._Owner._DoCommand('SET SMS %s SEEN' % self.Id)
 
    def Send(self):
        """Sends this SMS message.
        """
        self._Alter('SEND')

    def _GetBody(self):
        return self._Property('BODY')

    def _SetBody(self, Value):
        self._Property('BODY', Value)

    Body = property(_GetBody, _SetBody,
    doc="""Text of this SMS message.

    :type: unicode
    """)

    def _GetChunks(self):
        return SmsChunkCollection(self, xrange(int(chop(self._Property('CHUNKING', Cache=False))[0])))

    Chunks = property(_GetChunks,
    doc="""Chunks of this SMS message. More than one if this is a multi-part message.

    :type: `SmsChunkCollection`
    """)

    def _GetDatetime(self):
        from datetime import datetime
        return datetime.fromtimestamp(self.Timestamp)

    Datetime = property(_GetDatetime,
    doc="""Timestamp of this SMS message as datetime object.

    :type: datetime.datetime
    """)

    def _GetFailureReason(self):
        return str(self._Property('FAILUREREASON'))

    FailureReason = property(_GetFailureReason,
    doc="""Reason an SMS message failed. Read this if `Status` == `enums.smsMessageStatusFailed`.

    :type: `enums`.smsFailureReason*
    """)

    def _GetId(self):
        return self._Handle

    Id = property(_GetId,
    doc="""Unique SMS message Id.

    :type: int
    """)

    def _GetIsFailedUnseen(self):
        return (self._Property('IS_FAILED_UNSEEN') == 'TRUE')

    IsFailedUnseen = property(_GetIsFailedUnseen,
    doc="""Tells if a failed SMS message was unseen.

    :type: bool
    """)

    def _GetPrice(self):
        return int(self._Property('PRICE'))

    Price = property(_GetPrice,
    doc="""SMS price. Expressed using `PricePrecision`. For a value expressed using `PriceCurrency`, use `PriceValue`.

    :type: int

    :see: `PriceCurrency`, `PricePrecision`, `PriceToText`, `PriceValue`
    """)

    def _GetPriceCurrency(self):
        return self._Property('PRICE_CURRENCY')

    PriceCurrency = property(_GetPriceCurrency,
    doc="""SMS price currency.

    :type: unicode

    :see: `Price`, `PricePrecision`, `PriceToText`, `PriceValue`
    """)

    def _GetPricePrecision(self):
        return int(self._Property('PRICE_PRECISION'))

    PricePrecision = property(_GetPricePrecision,
    doc="""SMS price precision.

    :type: int

    :see: `Price`, `PriceCurrency`, `PriceToText`, `PriceValue`
    """)

    def _GetPriceToText(self):
        return (u'%s %.3f' % (self.PriceCurrency, self.PriceValue)).strip()

    PriceToText = property(_GetPriceToText,
    doc="""SMS price as properly formatted text with currency.

    :type: unicode

    :see: `Price`, `PriceCurrency`, `PricePrecision`, `PriceValue`
    """)

    def _GetPriceValue(self):
        if self.Price < 0:
            return 0.0
        return float(self.Price) / (10 ** self.PricePrecision)

    PriceValue = property(_GetPriceValue,
    doc="""SMS price. Expressed in `PriceCurrency`.

    :type: float

    :see: `Price`, `PriceCurrency`, `PricePrecision`, `PriceToText`
    """)

    def _GetReplyToNumber(self):
        return str(self._Property('REPLY_TO_NUMBER'))

    def _SetReplyToNumber(self, Value):
        self._Property('REPLY_TO_NUMBER', Value)

    ReplyToNumber = property(_GetReplyToNumber, _SetReplyToNumber,
    doc="""Reply-to number for this SMS message.

    :type: str
    """)

    def _SetSeen(self, Value):
        from warnings import warn
        warn('SmsMessage.Seen = x: Use SmsMessage.MarkAsSeen() instead.', DeprecationWarning, stacklevel=2)
        if Value:
            self.MarkAsSeen()
        else:
            raise SkypeError(0, 'Seen can only be set to True')

    Seen = property(fset=_SetSeen,
    doc="""Set the read status of the SMS message. Accepts only True value.

    :type: bool

    :deprecated: Extremely unpythonic, use `MarkAsSeen` instead.
    """)

    def _GetStatus(self):
        return str(self._Property('STATUS'))

    Status = property(_GetStatus,
    doc="""SMS message status.

    :type: `enums`.smsMessageStatus*
    """)

    def _GetTargetNumbers(self):
        return tuple(split(self._Property('TARGET_NUMBERS'), ', '))

    def _SetTargetNumbers(self, Value):
        self._Property('TARGET_NUMBERS', ', '.join(Value))

    TargetNumbers = property(_GetTargetNumbers, _SetTargetNumbers,
    doc="""Target phone numbers.

    :type: tuple of str
    """)

    def _GetTargets(self):
        return SmsTargetCollection(self, split(self._Property('TARGET_NUMBERS'), ', '))

    Targets = property(_GetTargets,
    doc="""Target objects.

    :type: `SmsTargetCollection`
    """)

    def _GetTimestamp(self):
        return float(self._Property('TIMESTAMP'))

    Timestamp = property(_GetTimestamp,
    doc="""Timestamp of this SMS message.

    :type: float

    :see: `Datetime`
    """)

    def _GetType(self):
        return str(self._Property('TYPE'))

    Type = property(_GetType,
    doc="""SMS message type

    :type: `enums`.smsMessageType*
    """)


class SmsMessageCollection(CachedCollection):
    _CachedType = SmsMessage


class SmsChunk(Cached):
    """Represents a single chunk of a multi-part SMS message.
    """
    _ValidateHandle = int

    def __repr__(self):
        return Cached.__repr__(self, 'Id', 'Message')

    def _GetCharactersLeft(self):
        count, left = map(int, chop(self.Message._Property('CHUNKING', Cache=False)))
        if self.Id == count - 1:
            return left
        return 0

    CharactersLeft = property(_GetCharactersLeft,
    doc="""CharactersLeft.

    :type: int
    """)

    def _GetId(self):
        return self._Handle

    Id = property(_GetId,
    doc="""SMS chunk Id.

    :type: int
    """)

    def _GetMessage(self):
        return self._Owner

    Message = property(_GetMessage,
    doc="""SMS message associated with this chunk.

    :type: `SmsMessage`
    """)

    def _GetText(self):
        return self.Message._Property('CHUNK %s' % self.Id)

    Text = property(_GetText,
    doc="""Text (body) of this SMS chunk.

    :type: unicode
    """)


class SmsChunkCollection(CachedCollection):
    _CachedType = SmsChunk


class SmsTarget(Cached):
    """Represents a single target of a multi-target SMS message.
    """
    _ValidateHandle = str

    def __repr__(self):
        return Cached.__repr__(self, 'Number', 'Message')

    def _GetMessage(self):
        return self._Owner

    Message = property(_GetMessage,
    doc="""An SMS message object this target refers to.

    :type: `SmsMessage`
    """)

    def _GetNumber(self):
        return self._Handle

    Number = property(_GetNumber,
    doc="""Target phone number.

    :type: str
    """)

    def _GetStatus(self):
        for t in split(self.Message._Property('TARGET_STATUSES'), ', '):
            number, status = t.split('=')
            if number == self.Number:
                return str(status)

    Status = property(_GetStatus,
    doc="""Status of this target.

    :type: `enums`.smsTargetStatus*
    """)


class SmsTargetCollection(CachedCollection):
    _CachedType = SmsTarget
