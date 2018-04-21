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
    >>> r = Rake(ranking_metric=Metric.<ranking_metric>)

:copyright: (c) 2017 by Vishwas B Sharma.
:license: MIT, see LICENSE for more details.
"""

from .rake import Metric, Rake
