"""Tests for giphy.client."""
import unittest

from giphy.client import Giphy


class GiphyClientTestCase(unittest.TestCase):

    def test_get_random_term_returns_two_words(self):
        """get_random_term() will return two words."""
        client = Giphy("bla")

        words = client.get_random_term()

        self.assertEqual(len(words.split(" ")), 2)
