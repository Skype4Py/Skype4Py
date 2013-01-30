"""File transfers.
"""
__docformat__ = 'restructuredtext en'


import os

from utils import *


class FileTransfer(Cached):
    """Represents a file transfer.
    """
    _ValidateHandle = int

    def __repr__(self):
        return Cached.__repr__(self, 'Id')

    def _Alter(self, AlterName, Args=None):
        return self._Owner._Alter('FILETRANSFER', self.Id, AlterName, Args)

    def _Property(self, PropName, Set=None):
        return self._Owner._Property('FILETRANSFER', self.Id, PropName, Set)

    def _GetBytesPerSecond(self):
        return int(self._Property('BYTESPERSECOND'))

    BytesPerSecond = property(_GetBytesPerSecond,
    doc="""Transfer speed in bytes per second.

    :type: int
    """)

    def _GetBytesTransferred(self):
        return long(self._Property('BYTESTRANSFERRED'))

    BytesTransferred = property(_GetBytesTransferred,
    doc="""Number of bytes transferred.

    :type: long
    """)

    def _GetFailureReason(self):
        return str(self._Property('FAILUREREASON'))

    FailureReason = property(_GetFailureReason,
    doc="""Transfer failure reason.

    :type: `enums`.fileTransferFailureReason*
    """)

    def _GetFileName(self):
        return os.path.basename(self.FilePath)

    FileName = property(_GetFileName,
    doc="""Name of the transferred file.

    :type: str
    """)

    def _GetFilePath(self):
        return unicode2path(self._Property('FILEPATH'))

    FilePath = property(_GetFilePath,
    doc="""Full path to the transferred file.

    :type: str
    """)

    def _GetFileSize(self):
        return long(self._Property('FILESIZE'))

    FileSize = property(_GetFileSize,
    doc="""Size of the transferred file in bytes.

    :type: long
    """)

    def _GetFinishDatetime(self):
        from datetime import datetime
        return datetime.fromtimestamp(self.FinishTime)

    FinishDatetime = property(_GetFinishDatetime,
    doc="""File transfer end date and time.

    :type: datetime.datetime
    """)

    def _GetFinishTime(self):
        return float(self._Property('FINISHTIME'))

    FinishTime = property(_GetFinishTime,
    doc="""File transfer end timestamp.

    :type: float
    """)

    def _GetId(self):
        return self._Handle

    Id = property(_GetId,
    doc="""Unique file transfer Id.

    :type: int
    """)

    def _GetPartnerDisplayName(self):
        return self._Property('PARTNER_DISPNAME')

    PartnerDisplayName = property(_GetPartnerDisplayName,
    doc="""File transfer partner DisplayName.

    :type: unicode
    """)

    def _GetPartnerHandle(self):
        return str(self._Property('PARTNER_HANDLE'))

    PartnerHandle = property(_GetPartnerHandle,
    doc="""File transfer partner Skypename.

    :type: str
    """)

    def _GetStartDatetime(self):
        from datetime import datetime
        return datetime.fromtimestamp(self.StartTime)

    StartDatetime = property(_GetStartDatetime,
    doc="""File transfer start date and time.

    :type: datetime.datetime
    """)

    def _GetStartTime(self):
        return float(self._Property('STARTTIME'))

    StartTime = property(_GetStartTime,
    doc="""File transfer start timestamp.

    :type: float
    """)

    def _GetStatus(self):
        return str(self._Property('STATUS'))

    Status = property(_GetStatus,
    doc="""File transfer status.

    :type: `enums`.fileTransferStatus*
    """)

    def _GetType(self):
        return str(self._Property('TYPE'))

    Type = property(_GetType,
    doc="""File transfer type.

    :type: `enums`.fileTransferType*
    """)


class FileTransferCollection(CachedCollection):
    _CachedType = FileTransfer
