.. contents:: :local:

Introduction
==============

``Skype4Py`` is a Python library which allows you to control Skype client application.

It works on Windows, OSX and Linux platforms with Python 2.x versions.

Community
===========

`Support and issues on Github <https://github.com/awahlig/skype4py>`_.
Skype4Py is not a Skype™, not associated with Microsoft or Skype.
For questions you can also use `stackoveflow.com with skype4py tag <http://stackoverflow.com/questions/tagged/skype4py>`_. Do **not** go for ``developer.skype.com`` for support.

Orignal author: `Arkadiusz Wahlig <http://arkadiusz.wahlig.eu/>`_

Maintainer: `Mikko Ohtamaa <http://opensourcehacker.com>`_

Usage
=====

Everything that you should ever need is available as aliases in the ``Skype4Py`` package.
Import it using the standard form of the ``import`` statement:

::

    import Skype4Py

Importing the whole package into your script's namespace using ``from Skype4Py import *`` is
generally discouraged. You should also not access the modules in the package directly as they
are considered an implementation detail and may change in future versions without notice.

The package provides the following:

- Classes

 ``Skype4Py.Skype``, an alias for `Skype4Py.skype.Skype`

 ``Skype4Py.CallChannelManager``, an alias for `Skype4Py.callchannel.CallChannelManager`

- Constants

 Everything from the `Skype4Py.enums` module.

 ``platform``, either ``'windows'``, ``'posix'`` or ``'darwin'`` depending
 on the current platform (Windows, Linux, Mac OS X).

- Errors

 ``Skype4Py.SkypeError``, an alias for `Skype4Py.errors.SkypeError`

 ``Skype4Py.SkypeAPIError``, an alias for `Skype4Py.errors.SkypeAPIError`

The two classes exposed by the ``Skype4Py`` package are the only ones that are to be instantiated
directly. They in turn provide means of instantiating the remaining ones. They are also the only
classes that provide event handlers (for more information about events and how to use them, see
the `EventHandlingBase` class.

Every Skype4Py script instantiates at least the ``Skype4Py.Skype`` class which gives access to
the Skype client running currently in the system. Follow the `Skype4Py.skype.Skype` reference to
see what you can do with it.

**Warning!** While reading this documentation, it is important to keep in mind that everything
needed is in the top package level because the documentation refers to all objects in the places
they actually live.

Quick example
----------------

This short example connects to Skype client and prints the user's full name and the names of all the
contacts from the contacts list:

::

   import Skype4Py

   # Create an instance of the Skype class.
   skype = Skype4Py.Skype()

   # Connect the Skype object to the Skype client.
   skype.Attach()

   # Obtain some information from the client and print it out.
   print 'Your full name:', skype.CurrentUser.FullName
   print 'Your contacts:'
   for user in skype.Friends:
       print '    ', user.FullName

Note on the naming convention
--------------------------------

Skype4Py uses two different naming conventions. The first one applies to interfaces derived from
`Skype4COM <https://developer.skype.com/Docs/Skype4COM>`_, a COM library which was an inspiration for Skype4Py. This convention uses the ``CapCase``
scheme for class names, properties, methods and their arguments. The constants use the ``mixedCase``
scheme.

The second naming convention is more "Pythonic" and is used by all other parts of the package
including internal objects. It uses mostly the same ``CapCase`` scheme for class names (including
exception names) with a small difference in abbreviations. Where the first convention would use
a ``SkypeApiError`` name, the second one uses ``SkypeAPIError``. Other names including properties,
methods, arguments, variables and module names use lowercase letters with underscores.

Projects using Skype4Py
=========================

See `Sevabot - A Skype bot supporting integration with external services <https://github.com/opensourcehacker/sevabot>`_

Troubleshooting
================

Segfaults
--------------

If you get segfault on OSX make sure you are using `32-bit Python <http://stackoverflow.com/questions/2088569/how-do-i-force-python-to-be-32-bit-on-snow-leopard-and-other-32-bit-64-bit-quest>`_.

`Debugging segmentation faults with Python <http://wiki.python.org/moin/DebuggingWithGdb>`_.

Related gdb dump::

    Program received signal EXC_BAD_ACCESS, Could not access memory.
    Reason: KERN_INVALID_ADDRESS at address: 0x0000000001243b68
    0x00007fff8c12d878 in CFRetain ()
    (gdb) bt
    #0  0x00007fff8c12d878 in CFRetain ()
    #1  0x00000001007e07ec in ffi_call_unix64 ()
    #2  0x00007fff5fbfbb50 in ?? ()
    (gdb) c
    Continuing.

    Program received signal EXC_BAD_ACCESS, Could not access memory.
    Reason: KERN_INVALID_ADDRESS at address: 0x0000000001243b68
    0x00007fff8c12d878 in CFRetain ()

Skype4Py on for OSX 64-bit (all new OSX versions)
------------------------------------------------------

Currently Skype4Py must be installed and run using ``arch``
command to force compatibility with 32-bit Skype client application.

To install::

    arch -i386 pip install Skype4Py

Also when you run your application using Skype4Py prefix the run command with::

    arch -i386

Crashing on a startup on Ubuntu server
------------------------------------------------------

Segfault when starting up the bot::

      File "build/bdist.linux-i686/egg/Skype4Py/skype.py", line 250, in __init__
      File "build/bdist.linux-i686/egg/Skype4Py/api/posix.py", line 40, in SkypeAPI
      File "build/bdist.linux-i686/egg/Skype4Py/api/posix_x11.py", line 254, in __in                                    it__
    Skype4Py.errors.SkypeAPIError: Could not open XDisplay
    Segmentation fault (core dumped)

This usually means that your DISPLAY environment variable is wrong.

Try::

    export DISPLAY=:1

or::

    export DISPLAY=:0

depending on your configuration before running Sevabot.

Running unit tests
====================

Here is an example::

    virtualenv-2.7 venv  # Create venv
    source venv/bin/activate
    python setup.py develop  # Install Skype4Py in development mode
    cd unittests
    python skype4pytest.py  # Execute tests

Making a release
=================

`Use zest.releaser <http://opensourcehacker.com/2012/08/14/high-quality-automated-package-releases-for-python-with-zest-releaser/>`_

Example::

    virtualenv-2.7 venv  # Create venv
    source venv/bin/activate
    # Bump version in setup.py
    python setup.py develop  # Install Skype4Py in development mode
    pip install collective.checkdocs
    pthon setup.py checkdocs # Check .rst syntax
    easy_install zest.releaser
    fullrelease

Trademark notification
========================

Skype™, associated trademarks and logos and the “S” logo are trademarks of Skype. ``Skype4Py``
Python project is not affiliate of Skype or Microsoft corporation.




