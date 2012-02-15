#!/usr/bin/env python

from distutils.core import setup

description = 'A Django interface to the Python interface to the Akismet anti comment-spam API.'
setup(name='django-akismet',
      version='0.2.0',
      description=description,
      author='Michael Foord',
      author_email='michael@voidspace.org.uk',
      url='http://www.voidspace.org.uk/python/modules.shtml#akismet',
      py_modules=['akismet'],
     )
