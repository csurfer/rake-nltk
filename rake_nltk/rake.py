# -*- coding: utf-8 -*-
"""Implementation of Rapid Automatic Keyword Extraction algorithm.

As described in the paper `Automatic keyword extraction from individual
documents` by Stuart Rose, Dave Engel, Nick Cramer and Wendy Cowley.
"""

import string
from collections import Counter, defaultdict
from enum import Enum
from itertools import chain, groupby, product
from typing import Callable, DefaultDict, Dict, List, Optional, Set, Tuple

import nltk

# Readability type definitions.
Word = str
Sentence = str
Phrase = Tuple[str, ...]


class Metric(Enum):
    """Different metrics that can be used for ranking."""

    DEGREE_TO_FREQUENCY_RATIO = 0  # Uses d(w)/f(w) as the metric
    WORD_DEGREE = 1  # Uses d(w) alone as the metric
    WORD_FREQUENCY = 2  # Uses f(w) alone as the metric


class Rake:
    """Rapid Automatic Keyword Extraction Algorithm."""

    def __init__(
        self,
        stopwords: Optional[Set[str]] = None,
        punctuations: Optional[Set[str]] = None,
        language: str = 'english',
        ranking_metric: Metric = Metric.DEGREE_TO_FREQUENCY_RATIO,
        max_length: int = 100000,
        min_length: int = 1,
        include_repeated_phrases: bool = True,
        sentence_tokenizer: Optional[Callable[[str], List[str]]] = None,
        word_tokenizer: Optional[Callable[[str], List[str]]] = None,
    ):
        """Constructor.

        :param stopwords: Words to be ignored for keyword extraction.
        :param punctuations: Punctuations to be ignored for keyword extraction.
        :param language: Language to be used for stopwords.
        :param max_length: Maximum limit on the number of words in a phrase
                           (Inclusive. Defaults to 100000)
        :param min_length: Minimum limit on the number of words in a phrase
                           (Inclusive. Defaults to 1)
        :param include_repeated_phrases: If phrases repeat in phrase list consider
                            them as is without dropping any phrases for future
                            calculations. (Defaults to True) Ex: "Magic systems is
                            a company. Magic systems was founded by Raul".

                            If repeated phrases are allowed phrase list would be
                            [
                                (magic, systems), (company,), (magic, systems),
                                (founded,), (raul,)
                            ]

                            If they aren't allowed phrase list would be
                            [
                                (magic, systems), (company,),
                                (founded,), (raul,)
                            ]
        :param sentence_tokenizer: Tokenizer used to tokenize the text string into sentences.
        :param word_tokenizer: Tokenizer used to tokenize the sentence string into words.
        """
        # By default use degree to frequency ratio as the metric.
        if isinstance(ranking_metric, Metric):
            self.metric = ranking_metric
        else:
            self.metric = Metric.DEGREE_TO_FREQUENCY_RATIO

        # If stopwords not provided we use language stopwords by default.
        self.stopwords: Set[str]
        if stopwords:
            self.stopwords = stopwords
        else:
            self.stopwords = set(nltk.corpus.stopwords.words(language))

        # If punctuations are not provided we ignore all punctuation symbols.
        self.punctuations: Set[str]
        if punctuations:
            self.punctuations = punctuations
        else:
            self.punctuations = set(string.punctuation)

        # All things which act as sentence breaks during keyword extraction.
        self.to_ignore: Set[str] = set(chain(self.stopwords, self.punctuations))

        # Assign min or max length to the attributes
        self.min_length: int = min_length
        self.max_length: int = max_length

        # Whether we should include repeated phreases in the computation or not.
        self.include_repeated_phrases: bool = include_repeated_phrases

        # Tokenizers.
        self.sentence_tokenizer: Callable[[str], List[str]]
        if sentence_tokenizer:
            self.sentence_tokenizer = sentence_tokenizer
        else:
            self.sentence_tokenizer = nltk.tokenize.sent_tokenize
        self.word_tokenizer: Callable[[str], List[str]]
        if word_tokenizer:
            self.word_tokenizer = word_tokenizer
        else:
            self.word_tokenizer = nltk.tokenize.wordpunct_tokenize

        # Stuff to be extracted from the provided text.
        self.frequency_dist: Dict[Word, int]
        self.degree: Dict[Word, int]
        self.rank_list: List[Tuple[float, Sentence]]
        self.ranked_phrases: List[Sentence]

    def extract_keywords_from_text(self, text: str):
        """Method to extract keywords from the text provided.

        :param text: Text to extract keywords from, provided as a string.
        """
        sentences: List[Sentence] = self._tokenize_text_to_sentences(text)
        self.extract_keywords_from_sentences(sentences)

    def extract_keywords_from_sentences(self, sentences: List[Sentence]):
        """Method to extract keywords from the list of sentences provided.

        :param sentences: Text to extraxt keywords from, provided as a list
                          of strings, where each string is a sentence.
        """
        phrase_list: List[Phrase] = self._generate_phrases(sentences)
        self._build_frequency_dist(phrase_list)
        self._build_word_co_occurance_graph(phrase_list)
        self._build_ranklist(phrase_list)

    def get_ranked_phrases(self) -> List[Sentence]:
        """Method to fetch ranked keyword strings.

        :return: List of strings where each string represents an extracted
                 keyword string.
        """
        return self.ranked_phrases

    def get_ranked_phrases_with_scores(self) -> List[Tuple[float, Sentence]]:
        """Method to fetch ranked keyword strings along with their scores.

        :return: List of tuples where each tuple is formed of an extracted
                 keyword string and its score. Ex: (5.68, 'Four Scoures')
        """
        return self.rank_list

    def get_word_frequency_distribution(self) -> Dict[Word, int]:
        """Method to fetch the word frequency distribution in the given text.

        :return: Dictionary (defaultdict) of the format `word -> frequency`.
        """
        return self.frequency_dist

    def get_word_degrees(self) -> Dict[Word, int]:
        """Method to fetch the degree of words in the given text. Degree can be
        defined as sum of co-occurances of the word with other words in the
        given text.

        :return: Dictionary (defaultdict) of the format `word -> degree`.
        """
        return self.degree

    def _tokenize_text_to_sentences(self, text: str) -> List[Sentence]:
        """Tokenizes the given text string into sentences using the configured
        sentence tokenizer. Configuration uses `nltk.tokenize.sent_tokenize`
        by default.

        :param text: String text to tokenize into sentences.
        :return: List of sentences as per the tokenizer used.
        """
        return self.sentence_tokenizer(text)

    def _tokenize_sentence_to_words(self, sentence: Sentence) -> List[Word]:
        """Tokenizes the given sentence string into words using the configured
        word tokenizer. Configuration uses `nltk.tokenize.wordpunct_tokenize`
        by default.

        :param sentence: String sentence to tokenize into words.
        :return: List of words as per the tokenizer used.
        """
        return self.word_tokenizer(sentence)

    def _build_frequency_dist(self, phrase_list: List[Phrase]) -> None:
        """Builds frequency distribution of the words in the given body of text.

        :param phrase_list: List of List of strings where each sublist is a
                            collection of words which form a contender phrase.
        """
        self.frequency_dist = Counter(chain.from_iterable(phrase_list))

    def _build_word_co_occurance_graph(self, phrase_list: List[Phrase]) -> None:
        """Builds the co-occurance graph of words in the given body of text to
        compute degree of each word.

        :param phrase_list: List of List of strings where each sublist is a
                            collection of words which form a contender phrase.
        """
        co_occurance_graph: DefaultDict[Word, DefaultDict[Word, int]] = defaultdict(lambda: defaultdict(lambda: 0))
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

    def _build_ranklist(self, phrase_list: List[Phrase]):
        """Method to rank each contender phrase using the formula

              phrase_score = sum of scores of words in the phrase.
              word_score = d(w) or f(w) or d(w)/f(w) where d is degree
                           and f is frequency.

        :param phrase_list: List of List of strings where each sublist is a
                            collection of words which form a contender phrase.
        """
        self.rank_list = []
        for phrase in phrase_list:
            rank = 0.0
            for word in phrase:
                if self.metric == Metric.DEGREE_TO_FREQUENCY_RATIO:
                    rank += 1.0 * self.degree[word] / self.frequency_dist[word]
                elif self.metric == Metric.WORD_DEGREE:
                    rank += 1.0 * self.degree[word]
                else:
                    rank += 1.0 * self.frequency_dist[word]
            self.rank_list.append((rank, ' '.join(phrase)))
        self.rank_list.sort(reverse=True)
        self.ranked_phrases = [ph[1] for ph in self.rank_list]

    def _generate_phrases(self, sentences: List[Sentence]) -> List[Phrase]:
        """Method to generate contender phrases given the sentences of the text
        document.

        :param sentences: List of strings where each string represents a
                          sentence which forms the text.
        :return: Set of string tuples where each tuple is a collection
                 of words forming a contender phrase.
        """
        phrase_list: List[Phrase] = []
        # Create contender phrases from sentences.
        for sentence in sentences:
            word_list: List[Word] = [word.lower() for word in self._tokenize_sentence_to_words(sentence)]
            phrase_list.extend(self._get_phrase_list_from_words(word_list))

        # Based on user's choice to include or not include repeated phrases
        # we compute the phrase list and return it. If not including repeated
        # phrases, we only include the first occurance of the phrase and drop
        # the rest.
        if not self.include_repeated_phrases:
            unique_phrase_tracker: Set[Phrase] = set()
            non_repeated_phrase_list: List[Phrase] = []
            for phrase in phrase_list:
                if phrase not in unique_phrase_tracker:
                    unique_phrase_tracker.add(phrase)
                    non_repeated_phrase_list.append(phrase)
            return non_repeated_phrase_list

        return phrase_list

    def _get_phrase_list_from_words(self, word_list: List[Word]) -> List[Phrase]:
        """Method to create contender phrases from the list of words that form
        a sentence by dropping stopwords and punctuations and grouping the left
        words into phrases. Only phrases in the given length range (both limits
        inclusive) would be considered to build co-occurrence matrix. Ex:

        Sentence: Red apples, are good in flavour.
        List of words: ['red', 'apples', ",", 'are', 'good', 'in', 'flavour']
        List after dropping punctuations and stopwords.
        List of words: ['red', 'apples', *, *, good, *, 'flavour']
        List of phrases: [('red', 'apples'), ('good',), ('flavour',)]

        List of phrases with a correct length:
        For the range [1, 2]: [('red', 'apples'), ('good',), ('flavour',)]
        For the range [1, 1]: [('good',), ('flavour',)]
        For the range [2, 2]: [('red', 'apples')]

        :param word_list: List of words which form a sentence when joined in
                          the same order.
        :return: List of contender phrases honouring phrase length requirements
                 that are formed after dropping stopwords and punctuations.
        """
        groups = groupby(word_list, lambda x: x not in self.to_ignore)
        phrases: List[Phrase] = [tuple(group[1]) for group in groups if group[0]]
        return list(filter(lambda x: self.min_length <= len(x) <= self.max_length, phrases))
