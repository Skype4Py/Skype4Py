import Skype4Py

if __name__ == '__main__':
    skype = Skype4Py.Skype()
    skype.FriendlyName = 'main'
    skype.Attach()
    
    print 'Your Skypename:'
    print '   ', skype.CurrentUserHandle
    
    print 'Your contacts:'
    for user in skype.Friends:
        print '   ', user.Handle
