# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""Unit tests for Rake.py"""

from collections import defaultdict

import nltk

from rake_nltk import Metric, Rake

###########################################################

text = """Compatibility of systems of linear constraints
over the set of natural numbers. Criteria of compatibility of a system
of linear Diophantine equations, strict inequations, and nonstrict
inequations are considered. Upper bounds for components of a minimal
set of solutions and algorithms of construction of minimal generating
sets of solutions for all types of systems are given. These criteria
and the corresponding algorithms for constructing a minimal supporting
set of solutions can be used in solving all the considered types of
systems and systems of mixed types."""


def test_build_frequency_dist():
    r = Rake()

    phrase_list = [['red', 'apples'], ['good'], ['red'], ['flavour']]
    freq = defaultdict(lambda: 0)
    freq['apples'] = 1
    freq['good'] = 1
    freq['flavour'] = 1
    freq['red'] = 2
    r._build_frequency_dist(phrase_list)
    assert r.get_word_frequency_distribution() == freq


def test_build_word_co_occurance_graph():
    r = Rake()

    phrase_list = [['red', 'apples'], ['good'], ['red'], ['flavour']]
    degree = defaultdict(lambda: 0)
    degree['apples'] = 2
    degree['good'] = 1
    degree['flavour'] = 1
    degree['red'] = 3
    r._build_word_co_occurance_graph(phrase_list)
    assert r.get_word_degrees() == degree


def test_generate_phrases():
    r = Rake()

    sentences = [
        'Red apples, are good in flavour.',
        'Keywords, which we define as a sequence of one or more words, '
        + "provide a compact representation of a document's content",
        'Criteria of compatibility of a system of linear Diophantine ' + 'equations',
        'whose gloomy beams transfigured the village into a lunar '
        + 'encampment of glowing houses and streets of volcanic deserts '
        + 'every fifteen seconds ',
    ]
    phrase_list = [
        ('red', 'apples'),
        ('good',),
        ('flavour',),
        ('keywords',),
        ('define',),
        ('sequence',),
        ('one',),
        ('words',),
        ('provide',),
        ('compact', 'representation'),
        ('document',),
        ('content',),
        ('criteria',),
        ('compatibility',),
        ('system',),
        ('linear', 'diophantine', 'equations'),
        ('whose', 'gloomy', 'beams', 'transfigured'),
        ('village',),
        ('lunar', 'encampment'),
        ('glowing', 'houses'),
        ('streets',),
        ('volcanic', 'deserts', 'every', 'fifteen', 'seconds'),
    ]
    assert r._generate_phrases(sentences) == phrase_list


def test_generate_phrases_with_length_limit():
    sentences = [
        'Red apples, are good in flavour.',
        'Keywords, which we define as a sequence of one or more words, '
        + "provide a compact representation of a document's content",
        'Criteria of compatibility of a system of linear Diophantine ' + 'equations',
        'whose gloomy beams transfigured the village into a lunar '
        + 'encampment of glowing houses and streets of volcanic deserts '
        + 'every fifteen seconds ',
    ]

    # Consider phrases which have minimum of 2 words and max of 4
    r = Rake(min_length=2, max_length=4)
    phrase_list = [
        ('red', 'apples'),
        ('compact', 'representation'),
        ('linear', 'diophantine', 'equations'),
        ('whose', 'gloomy', 'beams', 'transfigured'),
        ('lunar', 'encampment'),
        ('glowing', 'houses'),
    ]
    assert r._generate_phrases(sentences) == phrase_list

    # Consider phrases which have minimum of 5 words and max of 5
    r = Rake(min_length=5, max_length=5)
    phrase_list = [('volcanic', 'deserts', 'every', 'fifteen', 'seconds')]
    assert r._generate_phrases(sentences) == phrase_list


def test_get_phrase_list_from_words():
    r = Rake()

    word_list = ['red', 'apples', ',', 'are', 'good', 'in', 'flavour']
    phrase_list = [('red', 'apples'), ('good',), ('flavour',)]
    assert r._get_phrase_list_from_words(word_list) == phrase_list

    word_list = [
        'keywords',
        ',',
        'which',
        'we',
        'define',
        'as',
        'a',
        'sequence',
        'of',
        'one',
        'or',
        'more',
        'words',
        ',',
        'provide',
        'a',
        'compact',
        'representation',
        'of',
        'a',
        'document',
        "'",
        's',
        'content',
    ]
    phrase_list = [
        ('keywords',),
        ('define',),
        ('sequence',),
        ('one',),
        ('words',),
        ('provide',),
        ('compact', 'representation'),
        ('document',),
        ('content',),
    ]
    assert r._get_phrase_list_from_words(word_list) == phrase_list


def test_extract_keywords_from_text_degree_to_frequency_metric():
    r = Rake()
    r.extract_keywords_from_text(text)
    ranked_phrases = [
        'minimal generating sets',
        'linear diophantine equations',
        'minimal supporting set',
        'minimal set',
        'linear constraints',
        'upper bounds',
        'strict inequations',
        'nonstrict inequations',
        'natural numbers',
        'mixed types',
        'corresponding algorithms',
        'considered types',
        'set',
        'types',
        'considered',
        'algorithms',
        'used',
        'systems',
        'systems',
        'systems',
        'systems',
        'system',
        'solving',
        'solutions',
        'solutions',
        'solutions',
        'given',
        'criteria',
        'criteria',
        'construction',
        'constructing',
        'components',
        'compatibility',
        'compatibility',
    ]
    assert r.get_ranked_phrases() == ranked_phrases
    assert [phrase for _, phrase in r.get_ranked_phrases_with_scores()] == ranked_phrases


def test_extract_keywords_from_text_word_degree_metric():
    r = Rake(ranking_metric=Metric.WORD_DEGREE)
    r.extract_keywords_from_text(text)
    ranked_phrases = [
        'minimal supporting set',
        'minimal set',
        'minimal generating sets',
        'linear diophantine equations',
        'considered types',
        'mixed types',
        'linear constraints',
        'strict inequations',
        'set',
        'nonstrict inequations',
        'types',
        'corresponding algorithms',
        'upper bounds',
        'systems',
        'systems',
        'systems',
        'systems',
        'natural numbers',
        'solutions',
        'solutions',
        'solutions',
        'considered',
        'algorithms',
        'criteria',
        'criteria',
        'compatibility',
        'compatibility',
        'used',
        'system',
        'solving',
        'given',
        'construction',
        'constructing',
        'components',
    ]
    assert r.get_ranked_phrases() == ranked_phrases
    assert [phrase for _, phrase in r.get_ranked_phrases_with_scores()] == ranked_phrases


def test_extract_keywords_from_text_word_frequency_metric():
    r = Rake(ranking_metric=Metric.WORD_FREQUENCY)
    r.extract_keywords_from_text(text)
    ranked_phrases = [
        'minimal supporting set',
        'minimal set',
        'minimal generating sets',
        'considered types',
        'systems',
        'systems',
        'systems',
        'systems',
        'mixed types',
        'linear diophantine equations',
        'types',
        'strict inequations',
        'solutions',
        'solutions',
        'solutions',
        'set',
        'nonstrict inequations',
        'linear constraints',
        'corresponding algorithms',
        'upper bounds',
        'natural numbers',
        'criteria',
        'criteria',
        'considered',
        'compatibility',
        'compatibility',
        'algorithms',
        'used',
        'system',
        'solving',
        'given',
        'construction',
        'constructing',
        'components',
    ]

    assert r.get_ranked_phrases() == ranked_phrases
    assert [phrase for _, phrase in r.get_ranked_phrases_with_scores()] == ranked_phrases


def test_load_portuguese_stopwords():
    r = Rake(language='portuguese')
    assert r.stopwords is not None


def test_rake_default_metric():
    r = Rake(ranking_metric=1)
    assert r.metric == Metric.DEGREE_TO_FREQUENCY_RATIO


def test_allow_repeated_phrases():
    sentences = ['Magic systems is a company.', 'Magic systems was built in a garage']
    expected_phrase_list_with_repetitions = [
        (
            'magic',
            'systems',
        ),
        ('company',),
        ('magic', 'systems'),
        ('built',),
        ('garage',),
    ]
    expected_phrase_list_without_repetitions = [
        (
            'magic',
            'systems',
        ),
        ('company',),
        ('built',),
        ('garage',),
    ]

    r = Rake()
    assert r._generate_phrases(sentences) == expected_phrase_list_with_repetitions

    r = Rake(include_repeated_phrases=True)
    assert r._generate_phrases(sentences) == expected_phrase_list_with_repetitions

    r = Rake(include_repeated_phrases=False)
    assert r._generate_phrases(sentences) == expected_phrase_list_without_repetitions


def test_sent_tokenizer_config():
    text = 'This is a sentence with a #sent hashtag. This is another sentence with a a@rake.com email address.'

    punct_tokenized_sentences = [
        'This is a sentence with a #sent hashtag.',
        'This is another sentence with a a@rake.com email address.',
    ]

    # Default.
    r = Rake()
    assert punct_tokenized_sentences == r._tokenize_text_to_sentences(text)

    # Punct tokenize.
    r = Rake(sentence_tokenizer=nltk.tokenize.sent_tokenize)
    assert punct_tokenized_sentences == r._tokenize_text_to_sentences(text)

    # Custom tokenizer.
    def custom_tokenizer(text):
        return text.split('with')

    r = Rake(sentence_tokenizer=custom_tokenizer)
    assert [
        'This is a sentence ',
        ' a #sent hashtag. This is another sentence ',
        ' a a@rake.com email address.',
    ] == r._tokenize_text_to_sentences(text)


def test_word_tokenizer_config():
    sentence = 'This is a cooool #dummysmiley: :-) :-P <3 and some arrows < > -> <--'

    punct_tokenized_words = [
        'This',
        'is',
        'a',
        'cooool',
        '#',
        'dummysmiley',
        ':',
        ':-)',
        ':-',
        'P',
        '<',
        '3',
        'and',
        'some',
        'arrows',
        '<',
        '>',
        '->',
        '<--',
    ]

    # Default
    r = Rake()
    assert punct_tokenized_words == r._tokenize_sentence_to_words(sentence)

    # Punct tokenize.
    r = Rake(word_tokenizer=nltk.tokenize.wordpunct_tokenize)
    assert punct_tokenized_words == r._tokenize_sentence_to_words(sentence)

    # Custom tokenizer. (Tweet)
    r = Rake(word_tokenizer=nltk.tokenize.TweetTokenizer().tokenize)
    assert [
        'This',
        'is',
        'a',
        'cooool',
        '#dummysmiley',
        ':',
        ':-)',
        ':-P',
        '<3',
        'and',
        'some',
        'arrows',
        '<',
        '>',
        '->',
        '<--',
    ] == r._tokenize_sentence_to_words(sentence)
