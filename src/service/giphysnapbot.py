"""GiphySnapBot class for running the game."""
import logging

from service.base import GiphySnapBotBase
from service.utils import parse_direct_mention


logger = logging.getLogger(__name__)


class GiphySnapBot(GiphySnapBotBase):
    """Class for running the GiphySnapBot game."""

    def handle_event(self, event):
        """Handle a slack event."""
        if event["type"] == "message" and "subtype" not in event:
            logger.debug("Handling message event: {}".format(event))
            user_id, message = parse_direct_mention(event["text"])
            if user_id == self.bot_id:
                self.send_message(message)
