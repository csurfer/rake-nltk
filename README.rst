rake-nltk
=========

|pypiv| |pyv| |Licence| |Build Status| |Coverage Status| |Thanks|

RAKE short for Rapid Automatic Keyword Extraction algorithm, is a domain
independent keyword extraction algorithm which tries to determine key
phrases in a body of text by analyzing the frequency of word appearance
and its co-occurance with other words in the text.

|Demo|

Setup
-----

Using pip
~~~~~~~~~

.. code:: bash

    pip install rake-nltk

Directly from the repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    git clone https://github.com/csurfer/rake-nltk.git
    python rake-nltk/setup.py install

Post setup
----------

If you see a stopwords error, it means that you do not have the corpus
`stopwords` downloaded from NLTK. You can download it using command below.

.. code:: bash

    python -c "import nltk; nltk.download('stopwords')"

Basic Usage
-----------

.. code:: python

    from rake_nltk import Rake

    r = Rake() # Uses stopwords for english from NLTK, and all puntuation characters.

    r.extract_keywords_from_text(<text to process>)

    r.get_ranked_phrases() # To get keyword phrases ranked highest to lowest.

Advanced Usage
--------------

.. code:: python

    from rake_nltk import Metric, Rake

    # To use it with a specific language supported by nltk.
    r = Rake(language=<language>)

    # If you want to provide your own set of stop words and punctuations to
    r = Rake(
        stopwords=<list of stopwords>,
        punctuations=<string of puntuations to ignore>
    )

    # If you want to control the metric for ranking. Paper uses d(w)/f(w) as the
    # metric. You can use this API with the following metrics:
    # 1. d(w)/f(w) (Default metric) Ratio of degree of word to its frequency.
    # 2. d(w) Degree of word only.
    # 3. f(w) Frequency of word only.

    r = Rake(ranking_metric=Metric.DEGREE_TO_FREQUENCY_RATIO)
    r = Rake(ranking_metric=Metric.WORD_DEGREE)
    r = Rake(ranking_metric=Metric.WORD_FREQUENCY)

References
----------

This is a python implementation of the algorithm as mentioned in paper
`Automatic keyword extraction from individual documents by Stuart Rose,
Dave Engel, Nick Cramer and Wendy Cowley`_

Why I chose to implement it myself?
-----------------------------------

-  It is extremely fun to implement algorithms by reading papers. It is
   the digital equivalent of DIY kits.
-  There are some rather popular implementations out there, in python(\ `aneesha/RAKE`_) and
   node(\ `waseem18/node-rake`_) but neither seemed to use the power of `NLTK`_. By making NLTK
   an integral part of the implementation I get the flexibility and power to extend it in other
   creative ways, if I see fit later, without having to implement everything myself.
-  I plan to use it in my other pet projects to come and wanted it to be
   modular and tunable and this way I have complete control.

Contributing
------------

Bug Reports and Feature Requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Please use `issue tracker`_ for reporting bugs or feature requests.

Development
~~~~~~~~~~~

Pull requests are most welcome.

Buy the developer a cup of coffee!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you found the utility helpful you can buy me a cup of coffee using

|Donate|

.. |Donate| image:: https://www.paypalobjects.com/webstatic/en_US/i/btn/png/silver-pill-paypal-44px.png
   :target: https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=3BSBW7D45C4YN&lc=US&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donate_SM%2egif%3aNonHosted

.. _Automatic keyword extraction from individual documents by Stuart Rose, Dave Engel, Nick Cramer and Wendy Cowley: https://www.researchgate.net/profile/Stuart_Rose/publication/227988510_Automatic_Keyword_Extraction_from_Individual_Documents/links/55071c570cf27e990e04c8bb.pdf
.. _aneesha/RAKE: https://github.com/aneesha/RAKE
.. _waseem18/node-rake: https://github.com/waseem18/node-rake
.. _NLTK: http://www.nltk.org/
.. _issue tracker: https://github.com/csurfer/rake-nltk/issues

.. |Build Status| image:: https://travis-ci.org/csurfer/rake-nltk.svg?branch=master
   :target: https://travis-ci.org/csurfer/rake-nltk
.. |Licence| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/csurfer/rake-nltk/master/LICENSE
.. |Coverage Status| image:: https://coveralls.io/repos/github/csurfer/rake-nltk/badge.svg?branch=master
   :target: https://coveralls.io/github/csurfer/rake-nltk?branch=master
.. |Demo| image:: http://i.imgur.com/wVOzU7y.gif
.. |pypiv| image:: https://img.shields.io/pypi/v/rake-nltk.svg
   :target: https://pypi.python.org/pypi/rake-nltk
.. |pyv| image:: https://img.shields.io/pypi/pyversions/rake-nltk.svg
   :target: https://pypi.python.org/pypi/rake-nltk
.. |Thanks| image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
   :target: https://saythanks.io/to/csurfer
