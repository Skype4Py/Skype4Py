#!/usr/bin/env python

import Skype4Py
import threading
import sys

# check arguments and print usage if needed
if len(sys.argv) != 3:
    print 'Usage: app2app_client.py <username> <message>'
    sys.exit(1)

# create event; we will need one since Skype4Py's event
# handlers are called asynchronously on a separate thread
event = threading.Event()

# class with our Skype event handlers
class SkypeEvents:
    # this handler is called when streams are opened or
    # closed, the streams argument contains a list of
    # all currently opened streams
    def ApplicationStreams(self, app, streams):
        # if streams is not empty then a stream to
        # the user was opened, we use its Write
        # method to send data; if streams is empty
        # then it means a stream was closed and we
        # can signal the main thread that we're done
        if streams:
            streams[0].Write(sys.argv[2])
        else:
            global event
            event.set()

    # this handler is called when data is sent over a
    # stream, the streams argument contains a list of
    # all currently sending streams
    def ApplicationSending(self, app, streams):
        # if streams is empty then it means that all
        # streams have finished sending data, since
        # we have only one, we disconnect it here;
        # this will cause ApplicationStreams event
        # to be called
        if not streams:
            app.Streams[0].Disconnect()

# instatinate Skype object and set our event handlers
skype = Skype4Py.Skype(Events=SkypeEvents())

# attach to Skype client
skype.Attach()

# obtain reference to Application object
app = skype.Application('App2AppServer')

# create application
app.Create()

# connect application to user specified by script args
app.Connect(sys.argv[1])

# wait until the event handlers do the job
event.wait()

# delete application
app.Delete()
