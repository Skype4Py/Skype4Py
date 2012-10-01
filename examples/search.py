#!/usr/bin/env python

import Skype4Py

# Instatinate Skype object, all further actions are done
# using this object.
skype = Skype4Py.Skype()

# Start Skype if it's not already running.
if not skype.Client.IsRunning:
    skype.Client.Start()

# Set our application name.
skype.FriendlyName = 'Skype4Py_Example'

# Attach to Skype. This may cause Skype to open a confirmation
# dialog.
skype.Attach()

# Set up an event handler.
def new_skype_status(status):
    # If Skype is closed and reopened, it informs us about it
    # so we can reattach.
    if status == Skype4Py.apiAttachAvailable:
        skype.Attach()
skype.OnAttachmentStatus = new_skype_status

# Search for users and display their Skype name, full name
# and country.
for user in skype.SearchForUsers('john doe'):
    print user.Handle, user.FullName, user.Country
