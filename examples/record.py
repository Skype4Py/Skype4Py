#!/usr/bin/python

import Skype4Py
import sys
import time

# This variable will get its actual value in OnCall handler
CallStatus = 0

# Here we define a set of call statuses that indicate a call has been either aborted or finished
CallIsFinished = set ([Skype4Py.clsFailed, Skype4Py.clsFinished, Skype4Py.clsMissed, Skype4Py.clsRefused, Skype4Py.clsBusy, Skype4Py.clsCancelled]);

def AttachmentStatusText(status):
    return skype.Convert.AttachmentStatusToText(status)

def CallStatusText(status):
    return skype.Convert.CallStatusToText(status)

WavFile = ''
OutFile = ''
# This handler is fired when status of Call object has changed
def OnCall(call, status):
    global CallStatus
    global WavFile
    global OutFile
    CallStatus = status
    print 'Call status: ' + CallStatusText(status)

    if (status == Skype4Py.clsEarlyMedia or status == Skype4Py.clsInProgress) and OutFile != '' :
        print ' recording ' + OutFile
        call.OutputDevice( Skype4Py.callIoDeviceTypeFile ,OutFile )
        OutFile=''

    if status == Skype4Py.clsInProgress and WavFile != '' :
        print ' playing ' + WavFile
        call.InputDevice( Skype4Py.callIoDeviceTypeFile ,WavFile )

HasConnected = False
def OnInputStatusChanged(call, status):
    global HasConnected
    print 'InputStatusChanged: ',call.InputDevice(),call,status
    print ' inputdevice: ',call.InputDevice()
    # Hang up if finished
    if status == True:
        HasConnected = True
    if status == False and HasConnected == True:
        print ' play finished'
        call.Finish()

# This handler is fired when Skype attatchment status changes
def OnAttach(status):
    print 'API attachment status: ' + AttachmentStatusText(status)
    if status == Skype4Py.apiAttachAvailable:
        skype.Attach()

# Let's see if we were started with a command line parameter..
try:
    CmdLine = sys.argv[1]
except:
    print 'Usage: python skypecall.py destination [wavtosend] [wavtorecord]'
    sys.exit()

try:
    WavFile = sys.argv[2]
except:
    WavFile = ''

try:
    OutFile = sys.argv[3]
except:
    OutFile = ''


# Creating Skype object and assigning event handlers..
skype = Skype4Py.Skype()
skype.OnAttachmentStatus = OnAttach
skype.OnCallStatus = OnCall
skype.OnCallInputStatusChanged = OnInputStatusChanged

# Starting Skype if it's not running already..
if not skype.Client.IsRunning:
    print 'Starting Skype..'
    skype.Client.Start()

# Attatching to Skype..
print 'Connecting to Skype..'
skype.Attach()

# Checking if what we got from command line parameter is present in our contact list
Found = False
for F in skype.Friends:
    if F.Handle == CmdLine:
        Found = True
        print 'Calling ' + F.Handle + '..'
        skype.PlaceCall(CmdLine)
        break
if not Found:
    print 'Call target not found in contact list'
    print 'Calling ' + CmdLine + ' directly.'
    skype.PlaceCall(CmdLine)

# Loop until CallStatus gets one of "call terminated" values in OnCall handler
while not CallStatus in CallIsFinished:
    time.sleep(0.1)
