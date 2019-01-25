"""Tests for rules."""
import unittest

from rules import number_of_words


class NumberOfWordsTestCase(unittest.TestCase):
    """Tests for rules."""

    def test_returns_the_number_of_words_in_a_string(self):
        """number_of_words() will return the number of words in `string`."""
        string = "there are four words"
        self.assertEqual(number_of_words(string), 4)
