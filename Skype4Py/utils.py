"""Utility functions and classes used internally by Skype4Py.
"""
__docformat__ = 'restructuredtext en'


import sys
import weakref
import threading
import logging
from new import instancemethod


__all__ = ['tounicode', 'path2unicode', 'unicode2path', 'chop', 'args2dict', 'quote',
           'split', 'cndexp', 'EventHandlingBase', 'Cached', 'CachedCollection']


def tounicode(s):
    """Converts a string to a unicode string. Accepts two types or arguments. An UTF-8 encoded
    byte string or a unicode string (in the latter case, no conversion is performed).

    :Parameters:
      s : str or unicode
        String to convert to unicode.

    :return: A unicode string being the result of the conversion.
    :rtype: unicode
    """
    if isinstance(s, unicode):
        return s
    return str(s).decode('utf-8')
    
    
def path2unicode(path):
    """Decodes a file/directory path from the current file system encoding to unicode.

    :Parameters:
      path : str
        Encoded path.

    :return: Decoded path.
    :rtype: unicode
    """
    return path.decode(sys.getfilesystemencoding())
    

def unicode2path(path):
    """Encodes a file/directory path from unicode to the current file system encoding.

    :Parameters:
      path : unicode
        Decoded path.

    :return: Encoded path.
    :rtype: str
    """
    return path.encode(sys.getfilesystemencoding())


def chop(s, n=1, d=None):
    """Chops initial words from a string and returns a list of them and the rest of the string.
    The returned list is guaranteed to be n+1 long. If too little words are found in the string,
    a ValueError exception is raised.

    :Parameters:
      s : str or unicode
        String to chop from.
      n : int
        Number of words to chop.
      d : str or unicode
        Optional delimiter. Any white-char by default.

    :return: A list of n first words from the string followed by the rest of the string (``[w1, w2,
             ..., wn, rest_of_string]``).
    :rtype: list of: str or unicode
    """

    spl = s.split(d, n)
    if len(spl) == n:
        spl.append(s[:0])
    if len(spl) != n + 1:
        raise ValueError('chop: Could not chop %d words from \'%s\'' % (n, s))
    return spl


def args2dict(s):
    """Converts a string or comma-separated 'ARG="a value"' or 'ARG=value2' strings
    into a dictionary.

    :Parameters:
      s : str or unicode
        Input string.

    :return: ``{'ARG': 'value'}`` dictionary.
    :rtype: dict
    """

    d = {}
    while s:
        t, s = chop(s, 1, '=')
        if s.startswith('"'):
            # XXX: This function is used to parse strings from Skype. The question is,
            # how does Skype escape the double-quotes. The code below implements the
            # VisualBasic technique ("" -> ").
            i = 0
            while True:
                i = s.find('"', i+1)
                try:
                    if s[i+1] != '"':
                        break
                    else:
                        i += 1
                except IndexError:
                    break
            if i > 0:
                d[t] = s[1:i].replace('""', '"')
                if s[i+1:i+3] == ', ':
                    i += 2
                s = s[i+1:]
            else:
                d[t] = s
                break
        else:
            i = s.find(', ')
            if i >= 0:
                d[t] = s[:i]
                s = s[i+2:]
            else:
                d[t] = s
                break
    return d


def quote(s, always=False):
    """Adds double-quotes to string if it contains spaces.

    :Parameters:
      s : str or unicode
        String to add double-quotes to.
      always : bool
        If True, adds quotes even if the input string contains no spaces.

    :return: If the given string contains spaces or <always> is True, returns the string enclosed in
             double-quotes. Otherwise returns the string unchanged.
    :rtype: str or unicode
    """

    if always or ' ' in s:
        return '"%s"' % s.replace('"', '""') # VisualBasic double-quote escaping.
    return s


def split(s, d=None):
    """Splits a string.

    :Parameters:
      s : str or unicode
        String to split.
      d : str or unicode
        Optional delimiter. Any white-char by default.

    :return: A list of words or ``[]`` if the string was empty.
    :rtype: list of str or unicode

    :note: This function works like ``s.split(d)`` except that it always returns an empty list
           instead of ``['']`` for empty strings.
    """

    if s:
        return s.split(d)
    return []


def cndexp(condition, truevalue, falsevalue):
    """Simulates a conditional expression known from C or Python 2.5.

    :Parameters:
      condition : any
        Tells what should be returned.
      truevalue : any
        Value returned if condition evaluates to True.
      falsevalue : any
        Value returned if condition evaluates to False.

    :return: Either truevalue or falsevalue depending on condition.
    :rtype: same as type of truevalue or falsevalue
    """

    if condition:
        return truevalue
    return falsevalue


class EventSchedulerThread(threading.Thread):
    def __init__(self, name, after, handlers, args, kwargs):
        """Initializes the object.
        
        :Parameters:
          name : str
            Event name.
          after : threading.Thread or None
            If not None, a thread that needs to end before this
            one starts.
          handlers : iterable
            Iterable of callable event handlers.
          args : tuple
            Positional arguments for the event handlers.
          kwargs : dict
            Keyword arguments for the event handlers.

        :note: When the thread is started (using the ``start`` method), it iterates over
               the handlers and calls them with the supplied arguments.
        """
        threading.Thread.__init__(self, name='Skype4Py %s event scheduler' % name)
        self.setDaemon(False)
        self.after = after
        self.handlers = handlers
        self.args = args
        self.kwargs = kwargs

    def run(self):
        if self.after:
            self.after.join()
            self.after = None # Remove the reference.
        for handler in self.handlers:
            handler(*self.args, **self.kwargs)


class EventHandlingBase(object):
    """This class is used as a base by all classes implementing event handlers.

    Look at known subclasses (above in epydoc) to see which classes will allow you to
    attach your own callables (event handlers) to certain events occurring in them.

    Read the respective classes documentations to learn what events are provided by them. The
    events are always defined in a class whose name consist of the name of the class it provides
    events for followed by ``Events``). For example class `Skype` provides events defined in
    `SkypeEvents`. The events class is always defined in the same module as the main class.

    The events class tells you what events you can assign your event handlers to, when do they
    occur and what arguments should your event handlers accept.

    There are three ways of attaching an event handler to an event.

    ``Events`` object
    =================

       Write your event handlers as methods of a class. The superclass of your class
       is not important for Skype4Py, it will just look for methods with appropriate names.
       The names of the methods and their arguments lists can be found in respective events
       classes (see above).

       Pass an instance of this class as the ``Events`` argument to the constructor of
       a class whose events you are interested in. For example:

       .. python::

           import Skype4Py

           class MySkypeEvents:
               def UserStatus(self, Status):
                   print 'The status of the user changed'

           skype = Skype4Py.Skype(Events=MySkypeEvents())
           
       If your application is build around a class, you may want to use is for Skype4Py
       events too. For example:
       
       .. python::
       
           import Skype4Py
           
           class MyApplication:
               def __init__(self):
                   self.skype = Skype4Py.Skype(Events=self)
                   
               def UserStatus(self, Status):
                   print 'The status of the user changed'
                   
       This lets you access the `Skype` object (``self.skype``) without using global
       variables.

       In both examples, the ``UserStatus`` method will be called when the status of the
       user currently logged into Skype is changed.

    ``On...`` properties
    ====================

       This method lets you use any callables as event handlers. Simply assign them to ``On...``
       properties (where "``...``" is the name of the event) of the object whose events you are
       interested in. For example:
       
       .. python::

           import Skype4Py

           def user_status(Status):
               print 'The status of the user changed'

           skype = Skype4Py.Skype()
           skype.OnUserStatus = user_status

       The ``user_status`` function will be called when the status of the user currently logged
       into Skype is changed.

       The names of the events and their arguments lists can be found in respective events
       classes (see above). Note that there is no ``self`` argument (which can be seen in the events
       classes) simply because our event handler is a function, not a method.

    ``RegisterEventHandler`` / ``UnregisterEventHandler`` methods
    =============================================================

       This method, like the second one, also lets you use any callables as event handlers. However,
       it also lets you assign many event handlers to a single event. This may be useful if for
       example you need to momentarily attach an event handler without disturbing other parts of
       your code already using one of the above two methods.

       In this case, you use `RegisterEventHandler` and `UnregisterEventHandler` methods
       of the object whose events you are interested in. For example:
       
       .. python::

           import Skype4Py

           def user_status(Status):
               print 'The status of the user changed'

           skype = Skype4Py.Skype()
           skype.RegisterEventHandler('UserStatus', user_status)

       The ``user_status`` function will be called when the status of the user currently logged
       into Skype is changed.

       The names of the events and their arguments lists should be taken from respective events
       classes (see above). Note that there is no ``self`` argument (which can be seen in the events
       classes) simply because our event handler is a function, not a method.
       
       All handlers attached to a single event will be called serially in the order they were
       registered.

    Multithreading warning
    ======================

       All event handlers are called on separate threads, never on the main one. At any given time,
       there is at most one thread per event calling your handlers. This means that when many events
       of the same type occur at once, the handlers will be called one after another. Different events
       will be handled simultaneously.
    
    Cyclic references note
    ======================

       Prior to Skype4Py 1.0.32.0, the library used weak references to the handlers. This was removed
       to avoid confusion and simplify/speed up the code. If cyclic references do occur, they are
       expected to be removed by the Python's garbage collector which should always be present as
       the library is expected to work in a relatively resource rich environment which is needed
       by the Skype client anyway.
    """
    # Initialized by the _AddEvents() class method.
    _EventNames = []

    def __init__(self):
        """Initializes the object.
        """
        # Event -> EventSchedulerThread object mapping. Use WeakValueDictionary to let the
        # threads be freed after they are finished.
        self._EventThreads = weakref.WeakValueDictionary()
        self._EventHandlerObject = None # Current "Events" object.
        self._DefaultEventHandlers = {} # "On..." handlers.
        self._EventHandlers = {} # "RegisterEventHandler" handlers.
        self.__Logger = logging.getLogger('Skype4Py.utils.EventHandlingBase')

        # Initialize the _EventHandlers mapping.
        for event in self._EventNames:
            self._EventHandlers[event] = []

    def _CallEventHandler(self, Event, *Args, **KwArgs):
        """Calls all event handlers defined for given Event, additional parameters
        will be passed unchanged to event handlers, all event handlers are fired on
        separate threads.
        
        :Parameters:
          Event : str
            Name of the event.
          Args
            Positional arguments for the event handlers.
          KwArgs
            Keyword arguments for the event handlers.
        """
        if Event not in self._EventHandlers:
            raise ValueError('%s is not a valid %s event name' % (Event, self.__class__.__name__))
        args = map(repr, Args) + ['%s=%s' % (key, repr(value)) for key, value in KwArgs.items()]
        self.__Logger.debug('calling %s: %s', Event, ', '.join(args))
        # Get a list of handlers for this event.
        try:
            handlers = [self._DefaultEventHandlers[Event]]
        except KeyError:
            handlers = []
        try:
            handlers.append(getattr(self._EventHandlerObject, Event))
        except AttributeError:
            pass
        handlers.extend(self._EventHandlers[Event])
        # Proceed only if there are handlers.
        if handlers:
            # Get the last thread for this event.
            after = self._EventThreads.get(Event, None)
            # Create a new thread, pass the last one to it so it can wait until it is finished.
            thread = EventSchedulerThread(Event, after, handlers, Args, KwArgs)
            # Store a weak reference to the new thread for this event.
            self._EventThreads[Event] = thread
            # Start the thread.
            thread.start()

    def RegisterEventHandler(self, Event, Target):
        """Registers any callable as an event handler.

        :Parameters:
          Event : str
            Name of the event. For event names, see the respective ``...Events`` class.
          Target : callable
            Callable to register as the event handler.

        :return: True is callable was successfully registered, False if it was already registered.
        :rtype: bool

        :see: `UnregisterEventHandler`
        """
        if not callable(Target):
            raise TypeError('%s is not callable' % repr(Target))
        if Event not in self._EventHandlers:
            raise ValueError('%s is not a valid %s event name' % (Event, self.__class__.__name__))
        if Target in self._EventHandlers[Event]:
            return False
        self._EventHandlers[Event].append(Target)
        self.__Logger.info('registered %s: %s', Event, repr(Target))
        return True

    def UnregisterEventHandler(self, Event, Target):
        """Unregisters an event handler previously registered with `RegisterEventHandler`.

        :Parameters:
          Event : str
            Name of the event. For event names, see the respective ``...Events`` class.
          Target : callable
            Callable to unregister.

        :return: True if callable was successfully unregistered, False if it wasn't registered
                 first.
        :rtype: bool

        :see: `RegisterEventHandler`
        """
        if not callable(Target):
            raise TypeError('%s is not callable' % repr(Target))
        if Event not in self._EventHandlers:
            raise ValueError('%s is not a valid %s event name' % (Event, self.__class__.__name__))
        if Target in self._EventHandlers[Event]:
            self._EventHandlers[Event].remove(Target)
            self.__Logger.info('unregistered %s: %s', Event, repr(Target))
            return True
        return False

    def _SetDefaultEventHandler(self, Event, Target):
        if Target:
            if not callable(Target):
                raise TypeError('%s is not callable' % repr(Target))
            self._DefaultEventHandlers[Event] = Target
            self.__Logger.info('set default %s: %s', Event, repr(Target))
        else:
            try:
                del self._DefaultEventHandlers[Event]
            except KeyError:
                pass

    def _GetDefaultEventHandler(self, Event):
        try:
            return self._DefaultEventHandlers[Event]
        except KeyError:
            return None

    def _SetEventHandlerObject(self, Object):
        """Registers an object as events handler, object should contain methods with names
        corresponding to event names, only one object may be registered at a time.
        
        :Parameters:
          Object
            Object to register. May be None in which case the currently registered object
            will be unregistered.
        """
        self._EventHandlerObject = Object
        self.__Logger.info('set object: %s', repr(Object))

    @classmethod
    def _AddEvents(cls, Class):
        """Adds events based on the attributes of the given ``...Events`` class.
        
        :Parameters:
          Class : class
            An `...Events` class whose methods define events that may occur in the
            instances of the current class.
        """
        def make_event(event):
            return property(lambda self: self._GetDefaultEventHandler(event),
                             lambda self, Value: self._SetDefaultEventHandler(event, Value))
        for event in dir(Class):
            if not event.startswith('_'):
                setattr(cls, 'On%s' % event, make_event(event))
                cls._EventNames.append(event)


class Cached(object):
    """Base class for all cached objects.

    Every object has an owning object a handle. Owning object is where the cache is
    maintained, handle identifies an object of given type.

    Thanks to the caching, trying to create two objects with the same owner and handle
    yields exactly the same object. The cache itself is based on weak references so
    not referenced objects are automatically removed from the cache.

    Because the ``__init__`` method will be called no matter if the object already
    existed or not, it is recommended to use the `_Init` method instead.
    """
    # Subclasses have to define a type/classmethod/staticmethod called
    # _ValidateHandle(Handle)
    # which is called by classmethod__new__ to validate the handle passed to
    # it before it is stored in the instance.

    def __new__(cls, Owner, Handle):
        Handle = cls._ValidateHandle(Handle)
        key = (cls, Handle)
        try:
            return Owner._ObjectCache[key]
        except KeyError:
            obj = object.__new__(cls)
            Owner._ObjectCache[key] = obj
            obj._Owner = Owner
            obj._Handle = Handle
            obj._Init()
            return obj
        except AttributeError:
            raise TypeError('%s is not a cached objects owner' % repr(Owner))
            
    def _Init(self):
        """Initializes the cached object. Receives all the arguments passed to the
        constructor The default implementation stores the ``Owner`` in
        ``self._Owner`` and ``Handle`` in ``self._Handle``.
        
        This method should be used instead of ``__init__`` to prevent double
        initialization.
        """

    def __copy__(self):
        return self
        
    def __repr__(self, *Attrs):
        if not Attrs:
            Attrs = ['_Handle']
        return '<%s.%s with %s>' % (self.__class__.__module__, self.__class__.__name__,
            ', '.join('%s=%s' % (name, repr(getattr(self, name))) for name in Attrs))
        
    def _MakeOwner(self):
        """Prepares the object for use as an owner for other cached objects.
        """
        self._CreateOwner(self)

    @staticmethod
    def _CreateOwner(Object):
        """Prepares any object for use as an owner for cached objects.
        
        :Parameters:
          Object
            Object that should be turned into a cached objects owner.
        """
        Object._ObjectCache = weakref.WeakValueDictionary()


class CachedCollection(object):
    """
    """
    _CachedType = Cached
    
    def __init__(self, Owner, Handles=[], Items=[]):
        self._Owner = Owner
        self._Handles = map(self._CachedType._ValidateHandle, Handles)
        for item in Items:
            self.append(item)

    def _AssertItem(self, Item):
        if not isinstance(Item, self._CachedType):
            raise TypeError('expected %s instance' % repr(self._CachedType))
        if self._Owner is not Item._Owner:
            raise TypeError('expected %s owned item' % repr(self._Owner))
        
    def _AssertCollection(self, Col):
        if not isinstance(Col, self.__class__):
            raise TypeError('expected %s instance' % repr(self.__class__))
        if self._CachedType is not Col._CachedType:
            raise TypeError('expected collection of %s' % repr(self._CachedType))
        if self._Owner is not Col._Owner:
            raise TypeError('expected %s owned collection' % repr(self._Owner))

    def __len__(self):
        return len(self._Handles)

    def __getitem__(self, Key):
        if isinstance(Key, slice):
            return self.__class__(self._Owner, self._Handles[Key])
        return self._CachedType(self._Owner, self._Handles[Key])

    def __setitem__(self, Key, Item):
        if isinstance(Key, slice):
            handles = []
            for it in Item:
                self._AssertItem(it)
                handles.append(it._Handle)
            self._Handlers[Key] = handles
        else:
            self._AssertItem(Item)
            self._Handles[Key] = Item._Handle

    def __delitem__(self, Key):
        del self._Handles[Key]

    def __iter__(self):
        for handle in self._Handles:
            yield self._CachedType(self._Owner, handle)

    def __contains__(self, Item):
        try:
            self._AssertItem(Item)
        except TypeError:
            return False
        return (Item._Handle in self._Handles)

    def __add__(self, Other):
        self._AssertCollection(Other)
        return self.__class__(self._Owner, self._Handles +
                          Other._Handles)

    def __iadd__(self, Other):
        self._AssertCollection(Other)
        self._Handles += Other._Handles
        return self

    def __mul__(self, Times):
        return self.__class__(self._Owner, self._Handles * Times)
    __rmul__ = __mul__

    def __imul__(self, Times):
        self._Handles *= Times
        return self
        
    def __copy__(self):
        obj = self.__class__(self._Owner)
        obj._Handles = self._Handles[:]
        return obj

    def append(self, item):
        """
        """
        self._AssertItem(item)
        self._Handles.append(item._Handle)

    def count(self, item):
        """
        """
        self._AssertItem(item)
        return self._Handles.count(item._Handle)

    def index(self, item):
        """
        """
        self._AssertItem(item)
        return self._Handles.index(item._Handle)

    def extend(self, seq):
        """
        """
        self.__iadd__(seq)

    def insert(self, index, item):
        """
        """
        self._AssertItem(item)
        self._Handles.insert(index, item._Handle)

    def pop(self, pos=-1):
        """
        """
        return self._CachedType(self._Owner, self._Handles.pop(pos))

    def remove(self, item):
        """
        """
        self._AssertItem(item)
        self._Handles.remove(item._Handle)

    def reverse(self):
        """
        """
        self._Handles.reverse()

    def sort(self, cmp=None, key=None, reverse=False):
        """
        """
        if key is None:
            wrapper = lambda x: self._CachedType(self._Owner, x)
        else:
            wrapper = lambda x: key(self._CachedType(self._Owner, x))
        self._Handles.sort(cmp, wrapper, reverse)

    def Add(self, Item):
        """
        """
        self.append(Item)

    def Remove(self, Index):
        """
        """
        del self[Index]

    def RemoveAll(self):
        """
        """
        del self[:]

    def Item(self, Index):
        """
        """
        return self[Index]

    def _GetCount(self):
        return len(self)

    Count = property(_GetCount,
    doc="""
    """)
