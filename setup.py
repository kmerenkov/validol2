#!/usr/bin/env python

#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2010 Konstantin Merenkov <kmerenkov@gmail.com>
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.


from distutils.core import setup

import validol2
import re

def get_version():
    return validol2.__version__

def get_author():
    return validol2.__author__

def get_author_email():
    author = get_author()
    re_email = re.compile(r'.*\<(?P<email>.+)\>.*')
    m = re_email.match(author)
    if m:
        return m.group('email')
    else:
        return None


setup(name='validol2',
      version=get_version(),
      description='',
      author=get_author(),
      maintainer=get_author(),
      author_email=get_author_email(),
      maintainer_email=get_author_email(),
      license='WTFPL version 2 (http://sam.zoy.org/wtfpl/)',
      url='http://github.com/kmerenkov/validol2/',
      py_modules=['validol2'])

