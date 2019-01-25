"""Tests for rules."""
import unittest

from rules import (
    any_match,
    illegal_words,
    number_of_words,
)


class NumberOfWordsTestCase(unittest.TestCase):
    """Tests for number_of_words()."""

    def test_returns_the_number_of_words_in_a_string(self):
        """Will return the number of words in `string`."""
        string = "there are four words"
        self.assertEqual(number_of_words(string), 4)

    def test_handles_more_than_one_space_between_words(self):
        """Will work when there is more than one space between words."""
        string = "I  have      lots    of space"
        self.assertEqual(number_of_words(string), 5)


class AnyMatchTestCase(unittest.TestCase):
    """Tests for any_match()."""

    def test_returns_false_if_no_words_match(self):
        """Will return false if none of the words match."""
        string_one = "one two three"
        string_two = "a b c"

        self.assertFalse(any_match(string_one, string_two))

    def test_returns_true_if_any_words_match(self):
        """Will return true if any of the words match."""
        string_one = "one two three"
        string_two = "a one c"

        self.assertTrue(any_match(string_one, string_two))

    def test_returns_true_if_complete_match(self):
        """Will return true if strings identical."""
        string = "one two three"

        self.assertTrue(any_match(string, string))

    def test_returns_false_if_string_is_none(self):
        """Will return false if any of the strings are None."""
        string_one = "one two three"
        string_two = None

        self.assertFalse(any_match(string_one, string_two))
        self.assertFalse(any_match(string_two, string_one))


class IllegalWordsTestCase(unittest.TestCase):
    """Tests for illegal_words()."""

    def test_returns_false_if_string_does_not_contain_illegal_word(self):
        """Will return false if the string does not contain an illegal word."""
        string = "one two three"

        self.assertFalse(illegal_words(string))

    def test_returns_true_if_string_contains_illegal_word(self):
        """Will return true if the string does contain an illegal word."""
        string = "one two swift"

        self.assertTrue(string)
