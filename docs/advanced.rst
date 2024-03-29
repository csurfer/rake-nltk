Usage Details
=============

Rake object accepts the following as the constructor parameters, by varying
which this implementation of Rake algorithm can be used for several different
purposes.

* stopwords : List of words which are considered to break sentences into
  phrases. Defaults to ``None``.
* punctuations : List of punctuations which are considered to break sentences
  into phrases. Defaults to ``None``.
* language : Language to use for tokenization and stopwords. Defaults to
  ``english``.
* ranking_metric : Metric to use for ranking of metrics
    * Ratio of degree of word to its frequency d(w)/f(w). (Default)
    * Degree of word only.
    * Frequency of word only.
* max_length : Of phrases to consider. Defaults to ``100000``.
* min_length : Of phrases to consider. Defaults to ``1``.

to use it with a specific language supported by nltk.
-----------------------------------------------------

.. code:: python

    from rake_nltk import Rake

    r = Rake(language=<language>)

Implementation automatically picks up the ``stopwords`` for that language and
default ``punctuation`` set.

to provide your own list of stop words and punctuations
-------------------------------------------------------

.. code:: python

    from rake_nltk import Rake

    r = Rake(
        stopwords=<list of stopwords>,
        punctuations=<string of puntuations to ignore>
    )

to control the metric for ranking
---------------------------------

.. code:: python

    from rake_nltk import Metric, Rake

    # Paper uses d(w)/f(w) as the final metric. You can use this API with the
    # following metrics:

    # 1. d(w)/f(w) (Default metric) Ratio of degree of word to its frequency.
    r = Rake(ranking_metric=Metric.DEGREE_TO_FREQUENCY_RATIO)

    # 2. d(w) Degree of word only.
    r = Rake(ranking_metric=Metric.WORD_DEGREE)

    # 3. f(w) Frequency of word only.
    r = Rake(ranking_metric=Metric.WORD_FREQUENCY)

to control the max or min words in a phrase
-------------------------------------------

So that only phrases of specific min and/or max lengthes are considered for
ranking

.. code:: python

    from rake_nltk import Rake

    r = Rake(min_length=2, max_length=4)

to control whether or not to include repeated phrases in text
-------------------------------------------------------------

So that user can choose to include all phrases generated from text or to
include phrases only once. Example: "Magic systems is a company. Magic systems
was founded in a garage" has the phrase (magic, systems) occuring twice.

.. code:: python

    from rake_nltk import Rake

    # To include all phrases even the repeated ones.
    r = Rake() # Equivalent to Rake(include_repeated_phrases=True)

    # To include all phrases only once and ignore the repetitions
    r = Rake(include_repeated_phrases=False)

to control the sentence tokenizer
---------------------------------

So that user can choose the sentence tokenizer they want to use.

.. code:: python

    from rake_nltk import Rake
    
    # To use default `nltk.tokenize.sent_tokenize` tokenizer.
    r = Rake() # Equivalent to Rake(sentence_tokenizer=nltk.tokenize.sent_tokenize)

    # To use a custom tokenizer.
    def custom_tokenizer(text: str) -> List[str]:
        ...
    r = Rake(sentence_tokenizer=custom_tokenizer)

to control the word tokenizer
---------------------------------

So that user can choose the word tokenizer they want to use.

.. code:: python

    from rake_nltk import Rake
    
    # To use default `nltk.tokenize.wordpunct_tokenize` tokenizer.
    r = Rake() # Equivalent to Rake(word_tokenizer=nltk.tokenize.wordpunct_tokenize)

    # To use a custom tokenizer.
    def custom_tokenizer(text: str) -> List[str]:
        ...
    r = Rake(word_tokenizer=custom_tokenizer)
