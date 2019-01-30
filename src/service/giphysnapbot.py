"""GiphySnapBot class for running the game."""
import logging

from service.base import (
    GiphySnapBotBase,
)
from service.utils import (
    is_direct_mention,
    is_invocation,
    parse_direct_mention,
    parse_invocation,
)
from rules import is_violation
from giphy.client import (
    Giphy,
    GiphyException,
)


logger = logging.getLogger(__name__)


START_GAME = "GIPHY GIPHY GIPHYSNAP GO!"
ACCEPTED_COMMANDS = [
    START_GAME,
]


class GiphySnapBot(GiphySnapBotBase):
    """Class for running the GiphySnapBot game."""

    def __init__(self, config):
        """Initalise GiphySnapBot and create a blank state."""
        super(GiphySnapBot, self).__init__(config)
        self.giphy_client = Giphy(config["giphy_api_key"])
        self.reset_state()

    def reset_state(self):
        """Reset game state."""
        logger.info("Reseting state")
        self.previous_player = None
        self.previous_term = None
        self.previous_url = None

    def start_game(self):
        logger.info("Starting new game")
        self.reset_state()
        term = self.giphy_client.get_random_term()

        try:
            gif = self.giphy_client.get_random_gif_for_term(term)
        except GiphyException:
            self.send_message("I couldn't find a gif for: {}".format(term))

        logger.debug("Starting new game with: {}".format(term))

        self.send_image(term, gif)

    def handle_event(self, event):
        """Handle a slack event."""
        if event["type"] != "message" or "subtype" in event:
            # not interested in non messages
            return

        logger.debug("Handling message event: {}".format(event))

        if is_direct_mention(event["text"]):
            logger.debug("Handling command")
            user_id, message = parse_direct_mention(event["text"])
            if user_id == self.bot_id:
                self.handle_command(message)
        if is_invocation(event):
            logger.debug("Handling invocation")

            term, url = parse_invocation(event)
            logger.debug("term: {}, url: {}".format(term, url))

            error = is_violation(self.previous_term, term)
            if error is not None:
                self.send_message("Infraction: {}".format(error))
                return

            if url == self.previous_url:
                self.send_message("Giphysnap!")
                self.reset_state()
            else:
                self.previous_term = term
                self.previous_url = url

        logger.debug(
            "Game State: {}, {}, {}".format(
                self.previous_player, self.previous_term, self.previous_url))

    def handle_command(self, command):
        """Handle a command directly to GiphySnapBot."""
        clean_command = command.strip()
        if clean_command in ACCEPTED_COMMANDS:
            if command == START_GAME:
                self.start_game()
        else:
            possible_commands = "\n".join(ACCEPTED_COMMANDS)
            self.send_message(
                "I don't know what you mean. Try:\n{}".format(
                    possible_commands))
