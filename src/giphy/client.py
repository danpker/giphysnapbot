import logging

import giphy_client
from random_word import RandomWords


logger = logging.getLogger(__name__)


class GiphyException(Exception):
    pass


class Giphy():

    def __init__(self, api_key):
        self._api_key = api_key
        self._api_instance = giphy_client.DefaultApi()
        self._random_words = RandomWords()
        logger.info("Started Giphy instance")

    def get_random_term(self):
        term = "{} {}".format(
            self._random_words.get_random_word(),
            self._random_words.get_random_word())
        return term

    def get_random_gif_for_term(self, term):
        api_response = self._api_instance.gifs_search_get(
            self._api_key, term, limit=1)
        if len(api_response.data) <= 0:
            logger.debug("Giphy couldn't find anything for: {}\n{}".format(
                term, api_response))
            raise GiphyException()

        return api_response.data[0].images.preview_gif.url
