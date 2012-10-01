#!/usr/bin/env python
# SkypeUsers.py

"""Displays the Skype contact list in a wxPython frame.
Clicking on a contact, pops up a dialog with user
details.
"""

import wx, wx.lib.dialogs
import Skype4Py
import sys, time

class MyFrame(wx.Frame):
  def __init__(self, *args, **kwds):
    # begin wxGlade: MyFrame.__init__
    kwds["style"] = wx.DEFAULT_FRAME_STYLE
    wx.Frame.__init__(self, *args, **kwds)
    self.contacts = wx.ListCtrl(self, -1,
        style=wx.LC_REPORT|wx.SUNKEN_BORDER)

    self.__set_properties()
    self.__do_layout()
    # end wxGlade

    # When the user dbl-clicks on a list item,
    # on_contact_clicked method will be called.
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,
        self.on_contact_clicked, self.contacts)

    # Create the Skype object.
    try:
      # Try using the DBus transport on Linux. Pass glib
      # mainloop to Skype4Py so it will use the wxPython
      # application glib mainloop to handle notifications
      # from Skype.
      from dbus.mainloop.glib import DBusGMainLoop
      self.skype = Skype4Py.Skype(Transport='dbus',
          MainLoop=DBusGMainLoop())
    except ImportError:
      # If the DBus couldn't be imported, use default
      # settings. This will work on Windows too.
      self.skype = Skype4Py.Skype()

    # Add columns to the contacts list control.
    self.contacts.InsertColumn(0, 'FullName', width=170)
    self.contacts.InsertColumn(1, 'Handle', width=130)
    self.contacts.InsertColumn(2, 'Country')

    # Create a list of Skype contacts sorted by their
    # FullNames.
    friends = list(self.skype.Friends)
    def fullname_lower(a, b):
      return -(a.FullName.lower() < b.FullName.lower())
    friends.sort(fullname_lower)

    # Add contacts to the list control.
    for user in friends:
      i = self.contacts.InsertStringItem(sys.maxint,
          user.FullName)
      self.contacts.SetStringItem(i, 1, user.Handle)
      self.contacts.SetStringItem(i, 2, user.Country)

    # When a user is focused in the Skype client, we will
    # focus it in our contact list too.
    self.skype.OnContactsFocused = \
        self.on_skype_contact_focused

  def __set_properties(self):
    # begin wxGlade: MyFrame.__set_properties
    self.SetTitle("Skype Test")
    # end wxGlade

  def __do_layout(self):
    # begin wxGlade: MyFrame.__do_layout
    sizer_1 = wx.BoxSizer(wx.VERTICAL)
    sizer_1.Add(self.contacts, 1, wx.EXPAND, 0)
    self.SetSizer(sizer_1)
    sizer_1.Fit(self)
    self.Layout()
    # end wxGlade

  def on_skype_contact_focused(self, username):
    # This will be called when a user is focused in Skype
    # client. We find him in our list control and select
    # the item.
    for i in range(self.contacts.GetItemCount()):
      # Since this event handler is called on a separate
      # thread, we have to use some synchronization
      # techniques like wx.CallAfter().
      wx.CallAfter(self.contacts.SetItemState, i, 0,
          wx.LIST_STATE_SELECTED)
      if self.contacts.GetItem(i, 1).GetText() == username:
        wx.CallAfter(self.contacts.SetItemState, i,
            wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

  def on_contact_clicked(self, event):
    # This will be called when a user is dbl-clicked in
    # the contact list control of our frame. We gather
    # the user details and display it in a dialog. We use
    # introspection to examine the Skype user object.

    # First we get user's Skypename from the list control
    # and we create a Skype user object based on it.
    user = self.skype.User(self.contacts.GetItem(event.GetIndex(), 1).GetText())

    # Now we traverse its properties and build
    # the details text.
    about = []
    for name in dir(user):
      value = getattr(user, name)
      if not name.startswith('_') and \
        not callable(value) and \
        value not in ([], '') and \
        name not in ('LastOnline',):
          if name == 'OnlineStatus':
            value = self.skype.Convert.OnlineStatusToText(value)
          elif name == 'Sex':
            value = self.skype.Convert.UserSexToText(value)
          about.append('%s: %s\n' % (name, value))
    about.sort()

    # Display a text dialog with user details.
    wx.lib.dialogs.scrolledMessageDialog(self, ''.join(about), 'About %s...' % user.FullName)

# end of class MyFrame


if __name__ == "__main__":
  # Initialize wxPython application and start
  # the main loop.
  app = wx.PySimpleApp(0)
  frame = MyFrame(None, -1, "")
  frame.SetSize((400, 500))
  app.SetTopWindow(frame)
  frame.Show()
  app.MainLoop()
