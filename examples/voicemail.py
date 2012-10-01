#!python

# ---------------------------------------------------------------------------------------------
#  Python / Skype4Py example that plays back last received voicemail
#
#  Tested with  Skype4Py version 0.9.28.2 and Skype verson 3.5.0.214

import sys
import time
import Skype4Py

def OnAttach(status): 
    print 'API attachment status: ' + skype.Convert.AttachmentStatusToText(status)
    if status == Skype4Py.apiAttachAvailable:
        skype.Attach()

skype = Skype4Py.Skype()
skype.OnAttachmentStatus = OnAttach

# Running Skype if its not running already..
if not skype.Client.IsRunning:
    print 'Starting Skype..'
    skype.Client.Start()

print 'Connecting to Skype..'
skype.Attach()

# Checking if we have any voicemails
if len(skype.Voicemails) == 0:
    print 'There are no voicemails.'
    sys.exit(0)

# Which voicemail has highest timestamp..
LastTimestamp = 0
for VM in skype.Voicemails:
    if VM.Timestamp > LastTimestamp:
        LastTimestamp = VM.Timestamp
        LastVoicemail = VM

# Displaying voicemail info and initiating playback        
print 'Last voicemail was received from ' + LastVoicemail.PartnerDisplayName
print 'Received : ' + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(LastVoicemail.Timestamp))
print 'Duration : ' + str(LastVoicemail.Duration) + ' seconds'

print 'Playing last voicemail..'
LastVoicemail.Open()

# Loop until playback gets finished
while not LastVoicemail.Status == "PLAYED":
    time.sleep(1);

print 'Playback is now finished.'
