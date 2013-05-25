#!/usr/bin/env python
"""
Skype4Py distutils script.

Copyright (c) 2007-2009, Arkadiusz Wahlig

All rights reserved.

Distributed under the BSD License, see the
accompanying LICENSE file for more information.
"""

import os
import sys

from setuptools import setup

from distutils.cmd import Command
from distutils.command.install_lib import install_lib as old_install_lib

VERSION = '1.0.35'

# Change the current dir to where the setup.py is in case we're not there.
path = os.path.split(sys.argv[0])[0]
if path:
    os.chdir(path)


# So that the Skype4Py library may know that the setup is running.
sys.skype4py_setup = True


class install_lib(old_install_lib):
    """Handles the 'install_lib' command.

    This modified version of install_lib command installs only the necessary
    platform modules from the Skype4Py.api subpackage.
    """

    def install(self):
        # The build is done here, now we have to adapt it to current platform
        # before installing.
        self.adapt_build_to_platform()

        # Let the original method do the hard work of copying the files.
        outfiles = old_install_lib.install(self)

        # Also byte_compile for distribution usage.
        if outfiles is not None:
            self.byte_compile(outfiles)

        return outfiles

    def adapt_build_to_platform(self):
        # We have to remove unneeded files from the build directory. First,
        # decide what platform we're on; this code is similar to the one
        # in Skype4Py/api/__init__.py which decides what submodule to
        # import at runtime.
        if sys.platform[:3] == 'win':
            platform = 'windows'
        elif sys.platform == 'darwin':
            platform = 'darwin'
        else:
            platform = 'posix'

        # Scan the <build_dir>/Skype4Py/api directory and remove all files
        # which names do not start with either '__' (for __init__) or the
        # detected platform.
        path = os.path.join(self.build_dir, os.path.join('Skype4Py', 'api'))
        for name in os.listdir(path):
            if not (name.startswith('__') or name.startswith(platform)):
                os.remove(os.path.join(path, name))


class build_doc(Command):
    """Handles the 'build_doc' command.

    This command builds the documentation using epydoc. The documentation is then
    zipped using zipfile standard module.
    """

    description = 'build the documentation'
    user_options = [('pdf', None, 'Builds a PDF documentation instead of a HTML one.')]

    def initialize_options(self):
        self.pdf = None

    def finalize_options(self):
        pass

    def run(self):
        try:
            from epydoc import cli

            epydoc_config = os.path.join('doc', 'epydoc.conf')

            old_argv = sys.argv[1:]
            try:
                sys.argv[1:] = ['--config=%s' % epydoc_config]
                if self.pdf:
                    sys.argv.append('--pdf')
                    sys.argv.append('--output=doc/pdf/')
                else:
                    sys.argv.append('--html')
                    sys.argv.append('--output=doc/html/')

                cli.cli()
            finally:
                sys.argv[1:] = old_argv

            print 'zipping the documentation'
            import zipfile
            if self.pdf:
                doctype = 'pdf'
            else:
                doctype = 'html'
            name = 'Skype4Py-%s-%sdoc' % (VERSION, doctype)
            z = zipfile.ZipFile(os.path.join('doc', '%s.zip' % name),
                    'w', zipfile.ZIP_DEFLATED)
            path = os.path.join('doc', doctype)
            if self.pdf:
                z.write(os.path.join(path, 'api.pdf'), '%s.pdf' % name)
            else:
                for f in os.listdir(path):
                    z.write(os.path.join(path, f), os.path.join(name, f))
            z.close()

        except ImportError:
            print >>sys.stderr, 'epydoc not installed, skipping build_doc.'


commands = {'build_doc': build_doc,
            'install_lib': install_lib}

desc = open("README.rst").read() + "\n" + open("CHANGES.rst").read()

# start the distutils setup
setup(name='Skype4Py',
      version=VERSION,
      description='Skype API wrapper for Python.',
      long_description=desc,
      author='Arkadiusz Wahlig',
      author_email='arkadiusz.wahlig@gmail.com',
      maintainer='Mikko Ohtamaa',
      url='https://github.com/awahlig/skype4py',
      license='BSD License',
      platforms=['Windows', 'Linux', 'MacOS X'],
      packages=['Skype4Py', 'Skype4Py.api', 'Skype4Py.lang'],
      provides=['Skype4Py'],
      install_requires=['setuptools'],
      zip_safe=True,
      cmdclass=commands)
