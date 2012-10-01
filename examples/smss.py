#!/usr/bin/env python

import Skype4Py

# instatinate Skype class
skype = Skype4Py.Skype()

# start Skype client if it isn't running
if not skype.Client.IsRunning:
    skype.Client.Start()

# list SMS messages
for sms in skype.Smss:
    print 'Sms Id:', sms.Id, 'time', sms.Timestamp
    print '  type:', sms.Type, \
        skype.Convert.SmsMessageTypeToText(sms.Type)
    print '  status:', sms.Status, \
        skype.Convert.SmsMessageStatusToText(sms.Status)
    print '  failure reason:', sms.FailureReason
    print '  failed unseen:', sms.IsFailedUnseen
    print '  price:', sms.Price
    print '  price precision:', sms.PricePrecision
    print '  price currency:', sms.PriceCurrency
    print '  reply to number:', sms.ReplyToNumber
    for target in sms.Targets:
        print '  target:', target.Number, 'status:', \
            skype.Convert.SmsTargetStatusToText(target.Status)
    print '  body: [%s]' % sms.Body
    for chunk in sms.Chunks:
        print '  chunk:', chunk.Id, '[%s]' % chunk.Text
