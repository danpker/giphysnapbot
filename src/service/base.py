"""Client service for Giphysnapbot."""
import time
import logging

from slackclient import SlackClient


RTM_READ_DELAY = 1  # 1 second delay between reading from RTM

logger = logging.getLogger(__name__)


class GiphySnapBotBase():
    """Base class for GiphySnapBot to hide connecting stuff."""

    def __init__(self, config):
        """Create a GiphySnapBotBase instance and connect to Slack."""
        self._slack_client = self._connect(config["slack_bot_token"])
        self.bot_id = self._get_user_id()
        self.default_channel = config["default_channel"]

    def _connect(self, slack_bot_token):
        """Connect to Slack and connect to the RTM API."""
        slack_client = SlackClient(slack_bot_token)
        connect_response = slack_client.rtm_connect(
            with_team_state=False, auto_reconnect=True)

        if connect_response:
            logger.info("RTM connected")
            return slack_client
        else:
            raise ConnectionError

    def _get_user_id(self):
        """Get the bot's user id from Slack."""
        auth_response = self._slack_client.api_call("auth.test")

        if auth_response.get("ok") is not None and auth_response["ok"]:
            bot_id = auth_response["user_id"]
            logger.info("Connected to slack with user id: {}".format(bot_id))
            return bot_id
        else:
            raise PermissionError(auth_response["error"])

    def run(self):
        """Run GiphySnapBot and handle_events."""
        while True:
            time.sleep(RTM_READ_DELAY)
            for event in self._slack_client.rtm_read():
                self.handle_event(event)

    def handle_event(self, event):
        """Handle the provided RTM events."""
        raise NotImplementedError(
            "handle_event() is not implemented for base class.")

    def send_message(self, message, channel=None):
        """Send `message` to `channel`."""
        if channel is None:
            channel = self.default_channel

        self._slack_client.api_call(
            "chat.postMessage", channel=channel, text=message)

    def send_image(self, title, url, channel=None):
        """Send an image to channle using attachments to `channel`."""
        if channel is None:
            channel = self.default_channel

        attachment = {
            "title": title,
            "image_url": url,
            "title_link": url,
        }
        self._slack_client.api_call(
            "chat.postMessage", channel=channel, attachment=[attachment])
