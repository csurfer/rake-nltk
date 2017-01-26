# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''Unit tests for Rake.py'''

__author__ = 'Vishwas B Sharma'
__author_email__ = 'sharma.vishwas88@gmail.com'
__version__ = '1.0.0'

import unittest
from collections import defaultdict

import nltk
from rake_nltk import Rake

###########################################################


class RakeUnitTest(unittest.TestCase):

    def test_build_frequency_dist(self):
        r = Rake()

        phrase_list = [['red', 'apples'], ['good'], ['red'], ['flavour']]
        freq = defaultdict(lambda: 0)
        freq['apples'] = 1
        freq['good'] = 1
        freq['flavour'] = 1
        freq['red'] = 2
        r._build_frequency_dist(phrase_list)
        self.assertEqual(r.get_word_frequency_distribution(), freq)

    def test_build_word_co_occurance_graph(self):
        r = Rake()

        phrase_list = [['red', 'apples'], ['good'], ['red'], ['flavour']]
        degree = defaultdict(lambda: 0)
        degree['apples'] = 2
        degree['good'] = 1
        degree['flavour'] = 1
        degree['red'] = 3
        r._build_word_co_occurance_graph(phrase_list)
        self.assertEqual(r.get_word_degrees(), degree)

    def test_generate_phrases(self):
        r = Rake()

        sentences = [
            'Red apples, are good in flavour.',
            'Keywords, which we define as a sequence of one or more words, ' +
            'provide a compact representation of a document\'s content'
        ]
        phrase_list = {('red', 'apples'), ('good',), ('flavour',), ('keywords',),
                       ('define',), ('sequence',), ('one',), ('words',),
                       ('provide',), ('compact', 'representation'), ('document',),
                       ('content',)}
        self.assertEqual(r._generate_phrases(sentences), phrase_list)

    def test_get_phrase_list_from_words(self):
        r = Rake()

        word_list = ['red', 'apples', ",", 'are', 'good', 'in', 'flavour']
        phrase_list = [('red', 'apples'), ('good',), ('flavour',)]
        self.assertEqual(r._get_phrase_list_from_words(word_list), phrase_list)

        word_list = ['keywords', ",", 'which', 'we', 'define', 'as', 'a',
                     'sequence', 'of', 'one', 'or', 'more', 'words', ",",
                     'provide', 'a', 'compact', 'representation', 'of', 'a',
                     'document', '\'', 's', 'content']
        phrase_list = [('keywords',), ('define',), ('sequence',), ('one',),
                       ('words',), ('provide',), ('compact', 'representation'),
                       ('document',), ('content',)]
        self.assertEqual(r._get_phrase_list_from_words(word_list), phrase_list)

    def test_extract_keywords_from_text(self):
        r = Rake()

        text = '''Compatibility of systems of linear constraints over the set of
        natural numbers. Criteria of compatibility of a system of linear
        Diophantine equations, strict inequations, and nonstrict inequations are
        considered. Upper bounds for components of a minimal set of solutions
        and algorithms of construction of minimal generating sets of solutions
        for all types of systems are given. These criteria and the corresponding
        algorithms for constructing a minimal supporting set of solutions can be
        used in solving all the considered types of systems and systems of mixed
        types.'''

        r.extract_keywords_from_text(text)

        ranked_phrases = [
            'minimal generating sets', 'linear diophantine equations',
            'minimal supporting set', 'minimal set', 'linear constraints',
            'upper bounds', 'strict inequations', 'nonstrict inequations',
            'natural numbers', 'mixed types', 'corresponding algorithms',
            'considered types', 'set', 'types', 'considered', 'algorithms',
            'used', 'systems', 'system', 'solving', 'solutions', 'given',
            'criteria', 'construction', 'constructing', 'components',
            'compatibility'
        ]
        self.assertEqual(r.get_ranked_phrases(), ranked_phrases)
        self.assertEqual([phrase for _, phrase in r.get_ranked_phrases_with_scores()], ranked_phrases)


if __name__ == '__main__':
    unittest.main()
