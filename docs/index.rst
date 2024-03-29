.. rake_nltk documentation master file, created by
   sphinx-quickstart on Sun Jun 10 00:44:16 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

rake-nltk
=========

|pypiv| |pyv| |Build Status| |Coverage Status| |Licence| |Downloads|

RAKE short for Rapid Automatic Keyword Extraction algorithm, is a domain
independent keyword extraction algorithm which tries to determine key
phrases in a body of text by analyzing the frequency of word appearance
and its co-occurance with other words in the text.

|Demo|

Features
--------

* Ridiculously simple interface.
* Configurable word and sentence tokenizers, language based stop words etc
* Configurable ranking metric.

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

Quick Start
-----------

.. code:: python

    from rake_nltk import Rake

    # Uses stopwords for english from NLTK, and all puntuation characters by
    # default
    r = Rake()

    # Extraction given the text.
    r.extract_keywords_from_text(<text to process>)

    # Extraction given the list of strings where each string is a sentence.
    r.extract_keywords_from_sentences(<list of sentences>)

    # To get keyword phrases ranked highest to lowest.
    r.get_ranked_phrases()

    # To get keyword phrases ranked highest to lowest with scores.
    r.get_ranked_phrases_with_scores()

API Reference
-------------

If you are looking for information on a specific function, class or
method, this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api

User guide
----------

If you are looking for general information on choices you have and what choice
can lead to what action, this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   advanced

Debugging Setup
---------------

If you see a stopwords error, it means that you do not have the corpus
`stopwords` downloaded from NLTK. You can download it using command below.

.. code:: bash

    python -c "import nltk; nltk.download('stopwords')"

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

1. Checkout the repository.
2. Make your changes and add/update relavent tests.
3. Install **`poetry`** using **`pip install poetry`**.
4. Run **`poetry install`** to create project's virtual environment.
5. Run tests using **`poetry run tox`** (Any python versions which you don't have checked out will fail this). Fix failing tests and repeat.
6. Make documentation changes that are relavant.
7. Install **`pre-commit`** using **`pip install pre-commit`** and run **`pre-commit run --all-files`** to do lint checks.
8. Generate documentation using **`poetry run sphinx-build -b html docs/ docs/_build/html`**.
9. Generate **`requirements.txt`** for automated testing using **`poetry export --dev --without-hashes -f requirements.txt > requirements.txt`**.
10. Commit the changes and raise a pull request.

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

.. |Build Status| image:: https://github.com/csurfer/rake-nltk/actions/workflows/pytest.yml/badge.svg
   :target: https://github.com/csurfer/rake-nltk/actions
.. |Licence| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/csurfer/rake-nltk/master/LICENSE
.. |Coverage Status| image:: https://codecov.io/gh/csurfer/rake-nltk/branch/master/graph/badge.svg?token=ghRhWVec9X
   :target: https://codecov.io/gh/csurfer/rake-nltk
.. |Demo| image:: http://i.imgur.com/wVOzU7y.gif
.. |pypiv| image:: https://img.shields.io/pypi/v/rake-nltk.svg
   :target: https://pypi.python.org/pypi/rake-nltk
.. |pyv| image:: https://img.shields.io/pypi/pyversions/rake-nltk.svg
   :target: https://pypi.python.org/pypi/rake-nltk
.. |Downloads| image:: https://pepy.tech/badge/rake-nltk
   :target: https://pepy.tech/project/rake-nltk
