Changelog
======================

1.0.35 (2013-05-25)
-------------------

- Fixed Issue #16 [prajna-pranab]

  The Skype API generally responds to ALTER commands by echoing back the command, including
  any id associated with the command e.g.

  -> ALTER VOICEMAIL <id> action
  <- ALTER VOICEMAIL <id> action

  For some reason the API strips the chat id from the ALTER CHAT command when it responds
  but the code in the chat.py _Alter() method was expecting the command to be echoed back
  just as it had been sent.

- Updated Skype main window classname under Windows for Skype versions 5 and
  higher, to detect whether Skype is running [suurjaak]

1.0.34 (2013-01-30)
--------------------

- Reworked release system and egg structure to follow the best practices [miohtama]

- Merged all fixed done in a fork https://github.com/stigkj/Skype4Py [miohtama]

- Use standard pkg_distribution mechanism to expose the version numebr [miohtama]

- Skype4Py.platform

  Easy detection of what platform code Skype4Py is using currently.
  May be one of 'posix', 'windows' or 'darwin'.

- DBus is now a default Linux (posix) platform

  Both DBus and X11 transports have been improved to work better in GUI environments.
  This revealed, that a special initialization code must be executed if the X11
  transport is combined with the PyGTK GUI framework and possible other similar
  libraries. The DBus transport on the other hand, requires enabling only a single
  option. That and the fact, that DBus is a newer technology created to replace
  such old IPC techniques like X11 messaging, forced me to make it the default
  transport.

- RunMainLoop option for DBus transport and Mac OS X (darwin) platform

- Fixed CHANGES syntax so that zest.releaser understands it [miohtama]

1.0.33 (2013-01-30)

* were removed and replaced by a single "RunMainLoop" option. The same option has
  been added to Mac OS X platform transport.

* The default value (if option is not specified) is True which means that the
  transport will run an events loop on a separate thread to be able to receive
  and process messages from Skype (which result in Skype4Py event handlers being
  fired up).

* This option has to be set to False if the events loop is going to be run somewhere
  else - the primary example are GUI applications which use the events loop to
  process messages from the user interfaces.

* Trying to run two loops (one by the GUI framework and another one by Skype4Py)
  causes a lot of problems and unexpected behavior. When set to False, this option
  will tell Skype4Py to reuse the already running loop.

* Note that if no other loop is running and this option is False, Skype4Py will
  remain to function (commands may be send to Skype and replies are returned)
  but it won't receive notifications from the client and their corresponding
  events will never be fired up.

* unittests for the common parts

  Unittests were written for parts of Skype4Py code shared by all platforms and
  transports. This is roughly 80% of the codebase and include all classes and the
  code translating object methods/properties calls to Skype API commands.

* Call and Voicemail device methods support simultaneous devices correctly

  The CaptureMicDevice(), InputDevice() and OutputDevice() methods trio of
  Call and Voicemail objects support enabling of multiple devices at the
  same time. Previously, enabling one device disabled all the other.

* Collections

  Almost all collection types used by Skype4COM are now supported by Skype4Py too.
  Collection types were initially skipped as Python provides a comprehensive set
  of its own container types. However, since most objects are represented by Handles
  or Ids, it makes a lot of sense to create a custom container type holding the
  handles only and creating the objects on-the-fly as they are accessed. This
  is the main reason for introduction of collection types. They also support
  methods provided by their counterparts in Skype4COM world.

* Code cleanup and naming conventions

  The whole codebase has been reviewed and cleaned up. The naming convention for
  all objects (modules, classes, etc.) has been defined and implemented. It still
  is a mixed convention (uses two different conventions applied to different
  objects) but at least there is a standard now.

* String type policy

  Skype4Py now returns unicode only when it is needed. For example, Skypenames
  are plain strings now while chat messages (their bodies) remain in unicode.

  Also, if Skype4Py expects a unicode string from the user and a plain string
  is passed instead, it tries to decode it using the UTF-8 codec (as opposed
  to ASCII codec which was used previously).
