"""GiphySnapBot class for running the game."""
import logging

from service.base import GiphySnapBotBase
from service.utils import (
    is_direct_mention,
    parse_direct_mention,
)


logger = logging.getLogger(__name__)


START_GAME = "GIPHY GIPHY GIPHYSNAP GO!"
ACCEPTED_COMMANDS = [
    START_GAME,
]


class GiphySnapBot(GiphySnapBotBase):
    """Class for running the GiphySnapBot game."""

    def handle_event(self, event):
        """Handle a slack event."""
        if event["type"] != "message" or "subtype" in event:
            # not interested in non messages
            return

        logger.debug("Handling message event: {}".format(event))

        if is_direct_mention(event["text"]):
            user_id, message = parse_direct_mention(event["text"])
            if user_id == self.bot_id:
                self.handle_command(message)

    def handle_command(self, command):
        clean_command = command.strip()
        if clean_command in ACCEPTED_COMMANDS:
            if command == START_GAME:
                self.start_game()
        else:
            possible_commands = "\n".join(ACCEPTED_COMMANDS)
            self.send_message(
                "I don't know what you mean. Try:\n{}".format(
                    possible_commands))


