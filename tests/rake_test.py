# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""Unit tests for Rake.py"""

import unittest
from collections import defaultdict

from rake_nltk import Metric, Rake


###########################################################


class RakeUnitTest(unittest.TestCase):
    def setUp(self):
        self.text = """Compatibility of systems of linear constraints
        over the set of natural numbers. Criteria of compatibility of a system
        of linear Diophantine equations, strict inequations, and nonstrict
        inequations are considered. Upper bounds for components of a minimal
        set of solutions and algorithms of construction of minimal generating
        sets of solutions for all types of systems are given. These criteria
        and the corresponding algorithms for constructing a minimal supporting
        set of solutions can be used in solving all the considered types of
        systems and systems of mixed types."""

    def test_build_frequency_dist(self):
        r = Rake()

        phrase_list = [["red", "apples"], ["good"], ["red"], ["flavour"]]
        freq = defaultdict(lambda: 0)
        freq["apples"] = 1
        freq["good"] = 1
        freq["flavour"] = 1
        freq["red"] = 2
        r._build_frequency_dist(phrase_list)
        self.assertEqual(r.get_word_frequency_distribution(), freq)

    def test_build_word_co_occurance_graph(self):
        r = Rake()

        phrase_list = [["red", "apples"], ["good"], ["red"], ["flavour"]]
        degree = defaultdict(lambda: 0)
        degree["apples"] = 2
        degree["good"] = 1
        degree["flavour"] = 1
        degree["red"] = 3
        r._build_word_co_occurance_graph(phrase_list)
        self.assertEqual(r.get_word_degrees(), degree)

    def test_generate_phrases(self):
        r = Rake()

        sentences = [
            "Red apples, are good in flavour.",
            "Keywords, which we define as a sequence of one or more words, "
            + "provide a compact representation of a document's content",
            "Criteria of compatibility of a system of linear Diophantine "
            + "equations",
            "whose gloomy beams transfigured the village into a lunar "
            + "encampment of glowing houses and streets of volcanic deserts "
            + "every fifteen seconds ",
        ]
        phrase_list = {
            ("red", "apples"),
            ("good",),
            ("flavour",),
            ("keywords",),
            ("define",),
            ("sequence",),
            ("one",),
            ("words",),
            ("provide",),
            ("compact", "representation"),
            ("document",),
            ("content",),
            ("criteria",),
            ("compatibility",),
            ("system",),
            ("linear", "diophantine", "equations"),
            ("whose", "gloomy", "beams", "transfigured"),
            ("volcanic", "deserts", "every", "fifteen", "seconds"),
            ("lunar", "encampment"),
            ("glowing", "houses"),
            ("village",),
            ("streets",),
        }
        self.assertEqual(r._generate_phrases(sentences), phrase_list)

    def test_generate_phrases_with_length_limit(self):
        sentences = [
            "Red apples, are good in flavour.",
            "Keywords, which we define as a sequence of one or more words, "
            + "provide a compact representation of a document's content",
            "Criteria of compatibility of a system of linear Diophantine "
            + "equations",
            "whose gloomy beams transfigured the village into a lunar "
            + "encampment of glowing houses and streets of volcanic deserts "
            + "every fifteen seconds ",
        ]

        # Consider phrases which have minimum of 2 words and max of 4
        r = Rake(min_length=2, max_length=4)
        phrase_list = {
            ("red", "apples"),
            ("compact", "representation"),
            ("linear", "diophantine", "equations"),
            ("whose", "gloomy", "beams", "transfigured"),
            ("lunar", "encampment"),
            ("glowing", "houses"),
        }
        self.assertEqual(r._generate_phrases(sentences), phrase_list)

        # Consider phrases which have minimum of 5 words and max of 5
        r = Rake(min_length=5, max_length=5)
        phrase_list = {("volcanic", "deserts", "every", "fifteen", "seconds")}
        self.assertEqual(r._generate_phrases(sentences), phrase_list)

    def test_get_phrase_list_from_words(self):
        r = Rake()

        word_list = ["red", "apples", ",", "are", "good", "in", "flavour"]
        phrase_list = [("red", "apples"), ("good",), ("flavour",)]
        self.assertEqual(r._get_phrase_list_from_words(word_list), phrase_list)

        word_list = [
            "keywords",
            ",",
            "which",
            "we",
            "define",
            "as",
            "a",
            "sequence",
            "of",
            "one",
            "or",
            "more",
            "words",
            ",",
            "provide",
            "a",
            "compact",
            "representation",
            "of",
            "a",
            "document",
            "'",
            "s",
            "content",
        ]
        phrase_list = [
            ("keywords",),
            ("define",),
            ("sequence",),
            ("one",),
            ("words",),
            ("provide",),
            ("compact", "representation"),
            ("document",),
            ("content",),
        ]
        self.assertEqual(r._get_phrase_list_from_words(word_list), phrase_list)

    def test_extract_keywords_from_text_degree_to_frequency_metric(self):
        r = Rake()
        r.extract_keywords_from_text(self.text)
        ranked_phrases = [
            "minimal generating sets",
            "linear diophantine equations",
            "minimal supporting set",
            "minimal set",
            "linear constraints",
            "upper bounds",
            "strict inequations",
            "nonstrict inequations",
            "natural numbers",
            "mixed types",
            "corresponding algorithms",
            "considered types",
            "set",
            "types",
            "considered",
            "algorithms",
            "used",
            "systems",
            "system",
            "solving",
            "solutions",
            "given",
            "criteria",
            "construction",
            "constructing",
            "components",
            "compatibility",
        ]
        self.assertEqual(r.get_ranked_phrases(), ranked_phrases)
        self.assertEqual(
            [phrase for _, phrase in r.get_ranked_phrases_with_scores()],
            ranked_phrases,
        )

    def test_extract_keywords_from_text_word_degree_metric(self):
        r = Rake(ranking_metric=Metric.WORD_DEGREE)
        r.extract_keywords_from_text(self.text)
        ranked_phrases = [
            "minimal supporting set",
            "minimal set",
            "minimal generating sets",
            "linear diophantine equations",
            "considered types",
            "mixed types",
            "linear constraints",
            "strict inequations",
            "set",
            "nonstrict inequations",
            "types",
            "corresponding algorithms",
            "upper bounds",
            "natural numbers",
            "considered",
            "algorithms",
            "used",
            "systems",
            "system",
            "solving",
            "solutions",
            "given",
            "criteria",
            "construction",
            "constructing",
            "components",
            "compatibility",
        ]
        self.assertEqual(r.get_ranked_phrases(), ranked_phrases)
        self.assertEqual(
            [phrase for _, phrase in r.get_ranked_phrases_with_scores()],
            ranked_phrases,
        )

    def test_extract_keywords_from_text_word_frequency_metric(self):
        r = Rake(ranking_metric=Metric.WORD_FREQUENCY)
        r.extract_keywords_from_text(self.text)
        ranked_phrases = [
            "minimal supporting set",
            "minimal set",
            "minimal generating sets",
            "considered types",
            "mixed types",
            "linear diophantine equations",
            "types",
            "strict inequations",
            "set",
            "nonstrict inequations",
            "linear constraints",
            "corresponding algorithms",
            "upper bounds",
            "natural numbers",
            "considered",
            "algorithms",
            "used",
            "systems",
            "system",
            "solving",
            "solutions",
            "given",
            "criteria",
            "construction",
            "constructing",
            "components",
            "compatibility",
        ]
        self.assertEqual(r.get_ranked_phrases(), ranked_phrases)
        self.assertEqual(
            [phrase for _, phrase in r.get_ranked_phrases_with_scores()],
            ranked_phrases,
        )

    def test_load_portuguese_stopwords(self):
        r = Rake(language="portuguese")
        self.assertIsNotNone(r.stopwords)


if __name__ == "__main__":
    unittest.main()
