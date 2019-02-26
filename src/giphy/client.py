"""Code for a client to talk to the Giphy API."""
import logging

import giphy_client
from random_words import RandomWords


logger = logging.getLogger(__name__)


class GiphyException(Exception):
    """Exception class for Giphy errors."""

    pass


class Giphy():
    """Class to contain API information and run requests."""

    def __init__(self, api_key):
        """Create an API instance using the api_key."""
        self._api_key = api_key
        self._api_instance = giphy_client.DefaultApi()
        self._random_words = RandomWords()
        logger.info("Started Giphy instance")

    def get_random_term(self):
        """Return a random, two word phrase."""
        term = "{} {}".format(
            self._random_words.random_word(),
            self._random_words.random_word(),
        )
        return term

    def get_random_gif_for_term(self, term):
        """Return a random gif that matches the given term."""
        api_response = self._api_instance.gifs_search_get(
            self._api_key, term, limit=1)
        if len(api_response.data) <= 0:
            logger.debug("Giphy couldn't find anything for: {}\n{}".format(
                term, api_response))
            raise GiphyException()

        return api_response.data[0].images.preview_gif.url
