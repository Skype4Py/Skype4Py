"""Skype client user interface control.
"""
__docformat__ = 'restructuredtext en'


import weakref

from enums import *
from errors import SkypeError
from utils import *


class Client(object):
    """Represents a Skype client. Access using `skype.Skype.Client`.
    """

    def __init__(self, Skype):
        """__init__.

        :Parameters:
          Skype : `Skype`
            Skype
        """
        self._SkypeRef = weakref.ref(Skype)

    def ButtonPressed(self, Key):
        """This command sends a button pressed notification event.

        :Parameters:
          Key : str
            Button key [0-9, A-Z, #, \*, UP, DOWN, YES, NO, SKYPE, PAGEUP, PAGEDOWN].
        """
        self._Skype._DoCommand('BTN_PRESSED %s' % Key)

    def ButtonReleased(self, Key):
        """This command sends a button released notification event.

        :Parameters:
          Key : str
            Button key [0-9, A-Z, #, \*, UP, DOWN, YES, NO, SKYPE, PAGEUP, PAGEDOWN].
        """
        self._Skype._DoCommand('BTN_RELEASED %s' % Key)

    def CreateEvent(self, EventId, Caption, Hint):
        """Creates a custom event displayed in Skype client's events pane.

        :Parameters:
          EventId : unicode
            Unique identifier for the event.
          Caption : unicode
            Caption text.
          Hint : unicode
            Hint text. Shown when mouse hoovers over the event.

        :return: Event object.
        :rtype: `PluginEvent`
        """
        self._Skype._DoCommand('CREATE EVENT %s CAPTION %s HINT %s' % (tounicode(EventId),
            quote(tounicode(Caption)), quote(tounicode(Hint))))
        return PluginEvent(self._Skype, EventId)

    def CreateMenuItem(self, MenuItemId, PluginContext, CaptionText, HintText=u'', IconPath='', Enabled=True,
                       ContactType=pluginContactTypeAll, MultipleContacts=False):
        """Creates custom menu item in Skype client's "Do More" menus.

        :Parameters:
          MenuItemId : unicode
            Unique identifier for the menu item.
          PluginContext : `enums`.pluginContext*
            Menu item context. Allows to choose in which client windows will the menu item appear.
          CaptionText : unicode
            Caption text.
          HintText : unicode
            Hint text (optional). Shown when mouse hoovers over the menu item.
          IconPath : unicode
            Path to the icon (optional).
          Enabled : bool
            Initial state of the menu item. True by default.
          ContactType : `enums`.pluginContactType*
            In case of `enums.pluginContextContact` tells which contacts the menu item should appear
            for. Defaults to `enums.pluginContactTypeAll`.
          MultipleContacts : bool
            Set to True if multiple contacts should be allowed (defaults to False).

        :return: Menu item object.
        :rtype: `PluginMenuItem`
        """
        cmd = 'CREATE MENU_ITEM %s CONTEXT %s CAPTION %s ENABLED %s' % (tounicode(MenuItemId), PluginContext,
            quote(tounicode(CaptionText)), cndexp(Enabled, 'true', 'false'))
        if HintText:
            cmd += ' HINT %s' % quote(tounicode(HintText))
        if IconPath:
            cmd += ' ICON %s' % quote(path2unicode(IconPath))
        if MultipleContacts:
            cmd += ' ENABLE_MULTIPLE_CONTACTS true'
        if PluginContext == pluginContextContact:
            cmd += ' CONTACT_TYPE_FILTER %s' % ContactType
        self._Skype._DoCommand(cmd)
        return PluginMenuItem(self._Skype, MenuItemId, CaptionText, HintText, Enabled)

    def Focus(self):
        """Brings the client window into focus.
        """
        self._Skype._Api.allow_focus(self._Skype.Timeout)
        self._Skype._DoCommand('FOCUS')

    def Minimize(self):
        """Hides Skype application window.
        """
        self._Skype._DoCommand('MINIMIZE')

    def OpenAddContactDialog(self, Username=''):
        """Opens "Add a Contact" dialog.

        :Parameters:
          Username : str
            Optional Skypename of the contact.
        """
        self.OpenDialog('ADDAFRIEND', Username)

    def OpenAuthorizationDialog(self, Username):
        """Opens authorization dialog.

        :Parameters:
          Username : str
            Skypename of the user to authenticate.
        """
        self.OpenDialog('AUTHORIZATION', Username)

    def OpenBlockedUsersDialog(self):
        """Opens blocked users dialog.
        """
        self.OpenDialog('BLOCKEDUSERS')

    def OpenCallHistoryTab(self):
        """Opens call history tab.
        """
        self.OpenDialog('CALLHISTORY')

    def OpenConferenceDialog(self):
        """Opens create conference dialog.
        """
        self.OpenDialog('CONFERENCE')

    def OpenContactsTab(self):
        """Opens contacts tab.
        """
        self.OpenDialog('CONTACTS')

    def OpenDialog(self, Name, *Params):
        """Open dialog. Use this method to open dialogs added in newer Skype versions if there is no
        dedicated method in Skype4Py.

        :Parameters:
          Name : str
            Dialog name.
          Params : unicode
            One or more optional parameters.
        """
        self._Skype._Api.allow_focus(self._Skype.Timeout)
        params = filter(None, (str(Name),) + Params)
        self._Skype._DoCommand('OPEN %s' % tounicode(' '.join(params)))

    def OpenDialpadTab(self):
        """Opens dial pad tab.
        """
        self.OpenDialog('DIALPAD')

    def OpenFileTransferDialog(self, Username, Folder):
        """Opens file transfer dialog.

        :Parameters:
          Username : str
            Skypename of the user.
          Folder : str
            Path to initial directory.
        """
        self.OpenDialog('FILETRANSFER', Username, 'IN', path2unicode(Folder))

    def OpenGettingStartedWizard(self):
        """Opens getting started wizard.
        """
        self.OpenDialog('GETTINGSTARTED')

    def OpenImportContactsWizard(self):
        """Opens import contacts wizard.
        """
        self.OpenDialog('IMPORTCONTACTS')

    def OpenLiveTab(self):
        """OpenLiveTab.
        """
        self.OpenDialog('LIVETAB')

    def OpenMessageDialog(self, Username, Text=u''):
        """Opens "Send an IM Message" dialog.

        :Parameters:
          Username : str
            Message target.
          Text : unicode
            Message text.
        """
        self.OpenDialog('IM', Username, tounicode(Text))

    def OpenOptionsDialog(self, Page=''):
        """Opens options dialog.

        :Parameters:
          Page : str
            Page name to open.

        :see: See https://developer.skype.com/Docs/ApiDoc/OPEN_OPTIONS for known Page values.
        """
        self.OpenDialog('OPTIONS', Page)

    def OpenProfileDialog(self):
        """Opens current user profile dialog.
        """
        self.OpenDialog('PROFILE')

    def OpenSearchDialog(self):
        """Opens search dialog.
        """
        self.OpenDialog('SEARCH')

    def OpenSendContactsDialog(self, Username=''):
        """Opens send contacts dialog.

        :Parameters:
          Username : str
            Optional Skypename of the user.
        """
        self.OpenDialog('SENDCONTACTS', Username)

    def OpenSmsDialog(self, SmsId):
        """Opens SMS window

        :Parameters:
          SmsId : int
            SMS message Id.
        """
        self.OpenDialog('SMS', str(SmsId))

    def OpenUserInfoDialog(self, Username):
        """Opens user information dialog.

        :Parameters:
          Username : str
            Skypename of the user.
        """
        self.OpenDialog('USERINFO', Username)

    def OpenVideoTestDialog(self):
        """Opens video test dialog.
        """
        self.OpenDialog('VIDEOTEST')

    def Shutdown(self):
        """Closes Skype application.
        """
        self._Skype._Api.shutdown()

    def Start(self, Minimized=False, Nosplash=False):
        """Starts Skype application.

        :Parameters:
          Minimized : bool
            If True, Skype is started minimized in system tray.
          Nosplash : bool
            If True, no splash screen is displayed upon startup.
        """
        self._Skype._Api.startup(Minimized, Nosplash)

    def _Get_Skype(self):
        skype = self._SkypeRef()
        if skype:
            return skype
        raise SkypeError('Skype4Py internal error')

    _Skype = property(_Get_Skype)

    def _GetIsRunning(self):
        return self._Skype._Api.is_running()

    IsRunning = property(_GetIsRunning,
    doc="""Tells if Skype client is running.

    :type: bool
    """)

    def _GetWallpaper(self):
        return unicode2path(self._Skype.Variable('WALLPAPER'))

    def _SetWallpaper(self, Value):
        self._Skype.Variable('WALLPAPER', path2unicode(Value))

    Wallpaper = property(_GetWallpaper, _SetWallpaper,
    doc="""Path to client wallpaper bitmap.

    :type: str
    """)

    def _GetWindowState(self):
        return str(self._Skype.Variable('WINDOWSTATE'))

    def _SetWindowState(self, Value):
        self._Skype.Variable('WINDOWSTATE', Value)

    WindowState = property(_GetWindowState, _SetWindowState,
    doc="""Client window state.

    :type: `enums`.wnd*
    """)


class PluginEvent(object):
    """Represents an event displayed in Skype client's events pane.
    """
    def __init__(self, Skype, Id):
        self._Skype = Skype
        self._Id = tounicode(Id)

    def __repr__(self):
        return '<%s with Id=%s>' % (object.__repr__(self)[1:-1], repr(self.Id))

    def Delete(self):
        """Deletes the event from the events pane in the Skype client.
        """
        self._Skype._DoCommand('DELETE EVENT %s' % self.Id)

    def _GetId(self):
        return self._Id

    Id = property(_GetId,
    doc="""Unique event Id.

    :type: unicode
    """)


class PluginMenuItem(object):
    """Represents a menu item displayed in Skype client's "Do More" menus.
    """
    def __init__(self, Skype, Id, Caption, Hint, Enabled):
        self._Skype = Skype
        self._Id = tounicode(Id)
        self._CacheDict = {}
        self._CacheDict['CAPTION'] = tounicode(Caption)
        self._CacheDict['HINT'] = tounicode(Hint)
        self._CacheDict['ENABLED'] = cndexp(Enabled, u'TRUE', u'FALSE')

    def __repr__(self):
        return '<%s with Id=%s>' % (object.__repr__(self)[1:-1], repr(self.Id))

    def _Property(self, PropName, Set=None):
        if Set is None:
            return self._CacheDict[PropName]
        self._Skype._Property('MENU_ITEM', self.Id, PropName, Set)
        self._CacheDict[PropName] = unicode(Set)

    def Delete(self):
        """Removes the menu item from the "Do More" menus.
        """
        self._Skype._DoCommand('DELETE MENU_ITEM %s' % self.Id)

    def _GetCaption(self):
        return self._Property('CAPTION')

    def _SetCaption(self, Value):
        self._Property('CAPTION', tounicode(Value))

    Caption = property(_GetCaption, _SetCaption,
    doc="""Menu item caption text.

    :type: unicode
    """)

    def _GetEnabled(self):
        return (self._Property('ENABLED') == 'TRUE')

    def _SetEnabled(self, Value):
        self._Property('ENABLED', cndexp(Value, 'TRUE', 'FALSE'))

    Enabled = property(_GetEnabled, _SetEnabled,
    doc="""Defines whether the menu item is enabled when a user launches Skype. If no value is defined,
    the menu item will be enabled.

    :type: bool
    """)

    def _GetHint(self):
        return self._Property('HINT')

    def _SetHint(self, Value):
        self._Property('HINT', tounicode(Value))

    Hint = property(_GetHint, _SetHint,
    doc="""Menu item hint text.

    :type: unicode
    """)

    def _GetId(self):
        return self._Id

    Id = property(_GetId,
    doc="""Unique menu item Id.

    :type: unicode
    """)
