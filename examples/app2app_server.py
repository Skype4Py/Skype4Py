#!/usr/bin/env python

import Skype4Py
import time

# class with our Skype event handlers
class SkypeEvents:
    # this handler is called when there is some
    # data waiting to be read
    def ApplicationReceiving(self, app, streams):
        # streams contain all streams that have
        # some data, we scan all of them, read
        # and print the data out
        for s in streams:
            print s.Read()

# instatinate Skype object and set our event handlers
skype = Skype4Py.Skype(Events=SkypeEvents())

# attach to Skype client
skype.Attach()

# obtain reference to Application object
app = skype.Application('App2AppServer')

# create application
app.Create()

# wait forever until Ctrl+C (SIGINT) is issued
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass

# delete application
app.Delete()
