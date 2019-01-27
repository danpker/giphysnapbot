"""Client service for Giphysnapbot."""
from slackclient import SlackClient


class GiphySnapBotBase():
    """Base class for GiphySnapBot to hide connecting stuff."""

    def __init__(self, config):
        """Create a GiphySnapBotBase instance and connect to Slack."""
        self._slack_client = self._connect(config["slack_bot_token"])
        self._bot_id = self._get_user_id()

    def _connect(self, slack_bot_token):
        """Connect to Slack and connect to the RTM API."""
        slack_client = SlackClient(slack_bot_token)
        connect_response = slack_client.rtm_connect(
            with_team_state=False, auto_reconnect=True)

        if connect_response.get("ok") is not None and connect_response["ok"]:
            return slack_client
        else:
            raise ConnectionError(connect_response["error"])

    def _get_user_id(self):
        """Get the bot's user id from Slack."""
        auth_response = self._slack_client.api_call("auth.test")

        if auth_response.get("ok") is not None and auth_response["ok"]:
            return auth_response["user_id"]
        else:
            raise PermissionError(auth_response["error"])

    def send_message(self, channel, message):
        """Send `message` to `channel`."""
        self._slack_client.api_call(
            "chat.postMessage", channel=channel, text=message)

    def send_image(self, channel, title, url):
        """Send an image to channle using attachments to `channel`."""
        attachment = {
            "title": title,
            "image_url": url,
            "title_link": url,
        }
        self._slack_client.api_call(
            "chat.postMessage", channel=channel, attachment=[attachment])
