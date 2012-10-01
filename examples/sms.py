#!/usr/bin/env python

import Skype4Py
import time

# class with Skype4Py event handlers
class SkypeEvents:
    # message status event handler
    def SmsMessageStatusChanged(self, sms, status):
        print '>Sms', sms.Id, 'status', status, \
            skype.Convert.SmsMessageStatusToText(status)
        if status == Skype4Py.smsMessageStatusFailed:
            print sms.FailureReason

    # target status event handler
    def SmsTargetStatusChanged(self, target, status):
        print '>Sms', target.Message.Id, \
            'target', target.Number, 'status', status, \
            skype.Convert.SmsTargetStatusToText(status)

# instatinate event handlers and Skype class
skype = Skype4Py.Skype(Events=SkypeEvents())

# start Skype client if it isn't running
if not skype.Client.IsRunning:
    skype.Client.Start()

# send SMS message
sms = skype.SendSms('+1234567890', Body='Hello!')

# event handlers will be called while we're sleeping
time.sleep(60)
