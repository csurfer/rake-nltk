# -*- coding: utf-8 -*-

#                __                    ____  __
#    _________ _/ /_____        ____  / / /_/ /__
#   / ___/ __ `/ //_/ _ \______/ __ \/ / __/ //_/
#  / /  / /_/ / ,< /  __/_____/ / / / / /_/ ,<
# /_/   \__,_/_/|_|\___/     /_/ /_/_/\__/_/|_|


"""
rake-nltk module
~~~~~~~~~~~~~

Usage of Rake class:

    >>> from rake_nltk import Rake
    >>> r = Rake() # With language as English
    >>> r = Rake(language=<language>) # With language set to <language>

:copyright: (c) 2017 by Vishwas B Sharma.
:license: MIT, see LICENSE for more details.
"""

__title__ = 'rake-nltk'
__version__ = '1.0.1'
__author__ = 'Vishwas B Sharma'
__author_email__ = 'sharma.vishwas88@gmail.com'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 Vishwas B Sharma'

from .rake import Rake
