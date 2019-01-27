"""GiphySnapBot class for running the game."""
import re
import logging

from service.base import GiphySnapBotBase


MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


logger = logging.getLogger(__name__)


def parse_direct_mention(message_text):
    """Return a direction mention message."""
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the
    # remaining message
    empty = (None, None)
    return (matches.group(1), matches.group(2).strip()) if matches else empty


class GiphySnapBot(GiphySnapBotBase):
    """Class for running the GiphySnapBot game."""

    def handle_event(self, event):
        """Handle a slack event."""
        if event["type"] == "message" and "subtype" not in event:
            logger.debug("Handling message event: {}".format(event))
            user_id, message = parse_direct_mention(event["text"])
            if user_id == self.bot_id:
                self.send_message(message)
