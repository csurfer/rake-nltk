# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''Implementation of Rapid Automatic Keyword Extraction algorithm.

As described in the paper `Automatic keyword extraction from individual
documents` by Stuart Rose, Dave Engel, Nick Cramer and Wendy Cowley.
'''

__author__ = 'Vishwas B Sharma'
__author_email__ = 'sharma.vishwas88@gmail.com'
__version__ = '1.0.0'

import string
from collections import defaultdict
from itertools import chain, groupby, product

import nltk
from nltk.tokenize import wordpunct_tokenize

# Ensure NLTK punkt package exists.
try:
    _ = nltk.tokenize.word_tokenize('Test string.')
except Exception:
    nltk.download('punkt')
# Ensure NLTK english.pickle exists.
try:
    _ = nltk.corpus.stopwords.words('english')
except Exception:
    nltk.download('stopwords')


class Rake(object):

    def __init__(self, stopwords=None, punctuations=None):
        '''Constructor.

           @param stopwords: List of Words to be ignored for keyword extraction.
           @param punctuations: Punctuations to be ignored for keyword
           extraction.
        '''
        # If stopwords not provided we use stopwords in english by default.
        self.stopwords = stopwords
        if self.stopwords is None:
            self.stopwords = nltk.corpus.stopwords.words('english')

        # If punctuations are not provided we ignore all punctuation symbols.
        self.punctuations = punctuations
        if self.punctuations is None:
            self.punctuations = list(string.punctuation)

        # All things which act as sentence breaks during keyword extraction.
        self.to_ignore = set(self.stopwords + self.punctuations)

        # Stuff to be extracted from the provided text.
        self.frequency_dist = None
        self.degree = None
        self.rank_list = None
        self.ranked_phrases = None

    def extract_keywords_from_text(self, text):
        '''Method to extract keywords from the text provided.

           @param text: Text to extract keywords from, provided as a string.
        '''
        sentences = nltk.tokenize.sent_tokenize(text)
        self.extract_keywords_from_sentences(sentences)

    def extract_keywords_from_sentences(self, sentences):
        '''Method to extract keywords from the list of sentences provided.

           @param sentences: Text to extraxt keywords from, provided as a list
           of strings, where each string is a sentence.
        '''
        phrase_list = self._generate_phrases(sentences)
        self._build_frequency_dist(phrase_list)
        self._build_word_co_occurance_graph(phrase_list)
        self._build_ranklist(phrase_list)

    def get_ranked_phrases(self):
        '''Method to fetch ranked keyword strings.

           @return: List of strings where each string represents an extracted
           keyword string.
        '''
        return self.ranked_phrases

    def get_ranked_phrases_with_scores(self):
        '''Method to fetch ranked keyword strings along with their scores.

           @return: List of tuples where each tuple is formed of an extracted
           keyword string and its score. Ex: (5.68, 'Four Scoures')
        '''
        return self.rank_list

    def get_word_frequency_distribution(self):
        '''Method to fetch the word frequency distribution in the given
           text.

           @return: Dictionary (defaultdict) of the format `word -> frequency`.
        '''
        return self.frequency_dist

    def get_word_degrees(self):
        '''Method to fetch the degree of words in the given text. Degree can be
           defined as sum of co-occurances of the word with other words in the
           given text.

           @return: Dictionary (defaultdict) of the format `word -> degree`.
        '''
        return self.degree

    def _build_frequency_dist(self, phrase_list):
        '''Builds frequency distribution of the words in the given body of text.

           @param phrase_list: List of List of strings where each sublist is a
           collection of words which form a contender phrase.
        '''
        self.frequency_dist = defaultdict(lambda: 0)
        for word in chain.from_iterable(phrase_list):
            self.frequency_dist[word] += 1

    def _build_word_co_occurance_graph(self, phrase_list):
        '''Builds the co-occurance graph of words in the given body of text to
           compute degree of each word.

           @param phrase_list: List of List of strings where each sublist is a
           collection of words which form a contender phrase.
        '''
        co_occurance_graph = defaultdict(lambda: defaultdict(lambda: 0))
        for phrase in phrase_list:
            # For each phrase in the phrase list, count co-occurances of the
            # word with other words in the phrase.
            #
            # Note: Keep the co-occurances graph as is, to help facilitate its
            # use in other creative ways if required later.
            for (word, coword) in product(phrase, phrase):
                co_occurance_graph[word][coword] += 1
        self.degree = defaultdict(lambda: 0)
        for key in co_occurance_graph:
            self.degree[key] = sum(co_occurance_graph[key].values())

    def _build_ranklist(self, phrase_list):
        '''Method to rank each contender phrase using the formula

              phrase_score = sum of scores of words in the phrase.
              word_score = d(w)/f(w) where d is degree and f is frequency.

           @param phrase_list: List of List of strings where each sublist is a
           collection of words which form a contender phrase.
        '''
        self.rank_list = []
        for phrase in phrase_list:
            rank = 0.0
            for word in phrase:
                rank += 1.0 * self.degree[word] / self.frequency_dist[word]
            self.rank_list.append((rank, ' '.join(phrase)))
        self.rank_list.sort(reverse=True)
        self.ranked_phrases = [ph[1] for ph in self.rank_list]

    def _generate_phrases(self, sentences):
        '''Method to generate contender phrases given the sentences of the text
           document.

           @param sentences: List of strings where each string represents a
           sentence which forms the text.
           @return: Set of string tuples where each tuple is a collection
           of words forming a contender phrase.
        '''
        phrase_list = set()
        # Create contender phrases from sentences.
        for sentence in sentences:
            word_list = [word.lower() for word in wordpunct_tokenize(sentence)]
            phrase_list.update(self._get_phrase_list_from_words(word_list))
        return phrase_list

    def _get_phrase_list_from_words(self, word_list):
        '''Method to create contender phrases from the list of words that form a
           sentence by dropping stopwords and punctuations and grouping the left
           words into phrases. Ex:

           Sentence: Red apples, are good in flavour.
           List of words: ['red', 'apples', ",", 'are', 'good', 'in', 'flavour']
           List after dropping punctuations and stopwords.
           List of words: ['red', 'apples', *, *, good, *, 'flavour']
           List of phrases: [('red', 'apples'), ('good',), ('flavour',)]

           @param word_list: List of words which form a sentence when joined in
           the same order.
           @return: List of contender phrases that are formed after dropping
           stopwords and punctuations.
        '''
        phrase_list = []
        for group in groupby(word_list, lambda x: x in self.to_ignore):
            if not group[0]:
                phrase_list.append(tuple(group[1]))
        return phrase_list
