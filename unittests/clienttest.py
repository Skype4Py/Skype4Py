import unittest

import skype4pytest
from Skype4Py.client import *


class ClientTest(skype4pytest.TestCase):
    def setUpObject(self):
        self.obj = self.skype.Client

    # Methods
    # =======

    def testButtonPressed(self):
        self.api.enqueue('BTN_PRESSED 5')
        self.obj.ButtonPressed('5')
        self.failUnless(self.api.is_empty())

    def testButtonReleased(self):
        self.api.enqueue('BTN_RELEASED 6')
        self.obj.ButtonReleased('6')
        self.failUnless(self.api.is_empty())

    def testCreateEvent(self):
        # Returned type: PluginEvent
        self.api.enqueue('CREATE EVENT spam CAPTION aCaption HINT aHint',
                         'EVENT spam CREATED')
        t = self.obj.CreateEvent('spam', 'aCaption', 'aHint')
        self.assertInstance(t, PluginEvent)
        self.assertEqual(t.Id, 'spam')
        self.failUnless(self.api.is_empty())

    def testCreateMenuItem(self):
        # Returned type: PluginMenuItem
        self.api.enqueue('CREATE MENU_ITEM spam CONTEXT CHAT CAPTION aCaption ENABLED true',
                         'MENU_ITEM spam CREATED')
        t = self.obj.CreateMenuItem('spam', 'CHAT', 'aCaption')
        self.assertInstance(t, PluginMenuItem)
        self.assertEqual(t.Id, 'spam')
        self.failUnless(self.api.is_empty())

    def testFocus(self):
        self.api.enqueue('FOCUS')
        self.obj.Focus()
        self.failUnless(self.api.is_empty())

    def testMinimize(self):
        self.api.enqueue('MINIMIZE')
        self.obj.Minimize()
        self.failUnless(self.api.is_empty())

    def testOpenAddContactDialog(self):
        self.api.enqueue('OPEN ADDAFRIEND spam')
        self.obj.OpenAddContactDialog('spam')
        self.failUnless(self.api.is_empty())

    def testOpenAuthorizationDialog(self):
        self.api.enqueue('OPEN AUTHORIZATION spam')
        self.obj.OpenAuthorizationDialog('spam')
        self.failUnless(self.api.is_empty())

    def testOpenBlockedUsersDialog(self):
        self.api.enqueue('OPEN BLOCKEDUSERS')
        self.obj.OpenBlockedUsersDialog()
        self.failUnless(self.api.is_empty())

    def testOpenCallHistoryTab(self):
        self.api.enqueue('OPEN CALLHISTORY')
        self.obj.OpenCallHistoryTab()
        self.failUnless(self.api.is_empty())

    def testOpenConferenceDialog(self):
        self.api.enqueue('OPEN CONFERENCE')
        self.obj.OpenConferenceDialog()
        self.failUnless(self.api.is_empty())

    def testOpenContactsTab(self):
        self.api.enqueue('OPEN CONTACTS')
        self.obj.OpenContactsTab()
        self.failUnless(self.api.is_empty())

    def testOpenDialog(self):
        self.api.enqueue('OPEN spam eggs')
        self.obj.OpenDialog('spam', 'eggs')
        self.failUnless(self.api.is_empty())

    def testOpenDialpadTab(self):
        self.api.enqueue('OPEN DIALPAD')
        self.obj.OpenDialpadTab()
        self.failUnless(self.api.is_empty())

    def testOpenFileTransferDialog(self):
        self.api.enqueue('OPEN FILETRANSFER spam IN eggs')
        self.obj.OpenFileTransferDialog('spam', 'eggs')
        self.failUnless(self.api.is_empty())

    def testOpenGettingStartedWizard(self):
        self.api.enqueue('OPEN GETTINGSTARTED')
        self.obj.OpenGettingStartedWizard()
        self.failUnless(self.api.is_empty())

    def testOpenImportContactsWizard(self):
        self.api.enqueue('OPEN IMPORTCONTACTS')
        self.obj.OpenImportContactsWizard()
        self.failUnless(self.api.is_empty())

    def testOpenLiveTab(self):
        self.api.enqueue('OPEN LIVETAB')
        self.obj.OpenLiveTab()
        self.failUnless(self.api.is_empty())

    def testOpenMessageDialog(self):
        self.api.enqueue('OPEN IM spam')
        self.obj.OpenMessageDialog('spam')
        self.failUnless(self.api.is_empty())

    def testOpenOptionsDialog(self):
        self.api.enqueue('OPEN OPTIONS')
        self.obj.OpenOptionsDialog()
        self.failUnless(self.api.is_empty())

    def testOpenProfileDialog(self):
        self.api.enqueue('OPEN PROFILE')
        self.obj.OpenProfileDialog()
        self.failUnless(self.api.is_empty())

    def testOpenSearchDialog(self):
        self.api.enqueue('OPEN SEARCH')
        self.obj.OpenSearchDialog()
        self.failUnless(self.api.is_empty())

    def _testOpenSendContactsDialog(self):
        self.api.enqueue('OPENSENDCONTACTSDIALOG')
        self.obj.OpenSendContactsDialog()
        self.failUnless(self.api.is_empty())

    def testOpenSmsDialog(self):
        self.api.enqueue('OPEN SMS 1234')
        self.obj.OpenSmsDialog(1234)
        self.failUnless(self.api.is_empty())

    def testOpenUserInfoDialog(self):
        self.api.enqueue('OPEN USERINFO spam')
        self.obj.OpenUserInfoDialog('spam')
        self.failUnless(self.api.is_empty())

    def testOpenVideoTestDialog(self):
        self.api.enqueue('OPEN VIDEOTEST')
        self.obj.OpenVideoTestDialog()
        self.failUnless(self.api.is_empty())

    # Properties
    # ==========

    def testWallpaper(self):
        # Readable, Writable, Type: str
        self.api.enqueue('GET WALLPAPER',
                         'WALLPAPER eggs')
        t = self.obj.Wallpaper
        self.assertInstance(t, str)
        self.assertEqual(t, 'eggs')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET WALLPAPER eggs',
                         'WALLPAPER eggs')
        self.obj.Wallpaper = 'eggs'
        self.failUnless(self.api.is_empty())

    def testWindowState(self):
        # Readable, Writable, Type: str
        self.api.enqueue('GET WINDOWSTATE',
                         'WINDOWSTATE NORMAL')
        t = self.obj.WindowState
        self.assertInstance(t, str)
        self.assertEqual(t, 'NORMAL')
        self.failUnless(self.api.is_empty())
        self.api.enqueue('SET WINDOWSTATE MAXIMIZED',
                         'WINDOWSTATE MAXIMIZED')
        self.obj.WindowState = 'MAXIMIZED'
        self.failUnless(self.api.is_empty())


class PluginEventTest(skype4pytest.TestCase):
    def setUpObject(self):
        self.obj = PluginEvent(self.skype, 'spam')

    # Methods
    # =======

    def testDelete(self):
        self.api.enqueue('DELETE EVENT spam')
        self.obj.Delete()
        self.failUnless(self.api.is_empty())

    # Properties
    # ==========

    def testId(self):
        # Readable, Type: unicode
        t = self.obj.Id
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'spam')
        self.failUnless(self.api.is_empty())


class PluginMenuItemTest(skype4pytest.TestCase):
    def setUpObject(self):
        self.obj = PluginMenuItem(self.skype, 'spam', 'eggs', 'sausage', True)

    # Methods
    # =======

    def testDelete(self):
        self.api.enqueue('DELETE MENU_ITEM spam')
        self.obj.Delete()
        self.failUnless(self.api.is_empty())

    # Properties
    # ==========

    def testCaption(self):
        # Readable, Writable, Type: unicode
        t = self.obj.Caption
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'eggs')
        self.api.enqueue('SET MENU_ITEM spam CAPTION eggs',
                         'MENU_ITEM spam CAPTION eggs')
        self.obj.Caption = 'eggs'
        self.failUnless(self.api.is_empty())

    def testEnabled(self):
        # Readable, Writable, Type: bool
        t = self.obj.Enabled
        self.assertInstance(t, bool)
        self.assertEqual(t, True)
        self.api.enqueue('SET MENU_ITEM spam ENABLED FALSE',
                         'MENU_ITEM spam ENABLED FALSE')
        self.obj.Enabled = False
        self.failUnless(self.api.is_empty())

    def testHint(self):
        # Readable, Writable, Type: unicode
        t = self.obj.Hint
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'sausage')
        self.api.enqueue('SET MENU_ITEM spam HINT eggs',
                         'MENU_ITEM spam HINT eggs')
        self.obj.Hint = 'eggs'
        self.failUnless(self.api.is_empty())

    def testId(self):
        # Readable, Type: unicode
        t = self.obj.Id
        self.assertInstance(t, unicode)
        self.assertEqual(t, 'spam')


def suite():
    return unittest.TestSuite([
        unittest.defaultTestLoader.loadTestsFromTestCase(ClientTest),
        unittest.defaultTestLoader.loadTestsFromTestCase(PluginEventTest),
        unittest.defaultTestLoader.loadTestsFromTestCase(PluginMenuItemTest),
    ])


if __name__ == '__main__':
    unittest.main()
