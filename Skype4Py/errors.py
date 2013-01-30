"""Error classes.
"""
__docformat__ = 'restructuredtext en'


class SkypeAPIError(Exception):
    """Exception raised whenever there is a problem with connection between
    Skype4Py and Skype client. It can be subscripted in which case following
    information can be obtained:

    +-------+------------------------------+
    | Index | Meaning                      |
    +=======+==============================+
    |     0 | (unicode) Error description. |
    +-------+------------------------------+
    """

    def __init__(self, errstr):
        """__init__.

        :Parameters:
          errstr : unicode
            Error description.
        """
        Exception.__init__(self, str(errstr))


class SkypeError(Exception):
    """Raised whenever Skype client reports an error back to Skype4Py. It can be
    subscripted in which case following information can be obtained:

    +-------+------------------------------+
    | Index | Meaning                      |
    +=======+==============================+
    |     0 | (int) Error code. See below. |
    +-------+------------------------------+
    |     1 | (unicode) Error description. |
    +-------+------------------------------+

    :see: https://developer.skype.com/Docs/ApiDoc/Error_codes for more information about
          Skype error codes. Additionally an **error code 0** can be raised by Skype4Py
          itself.
    """

    def __init__(self, errno, errstr):
        """__init__.

        :Parameters:
          errno : int
            Error code.
          errstr : unicode
            Error description.
        """
        Exception.__init__(self, int(errno), str(errstr))

    def __str__(self):
        return '[Errno %d] %s' % (self[0], self[1])
