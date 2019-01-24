import os
import re
import time

from slackclient import SlackClient
from random_word import RandomWords
import giphy_client


# Initialise APIs and stuff
r = RandomWords()
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
api_instance = giphy_client.DefaultApi()
api_key = os.environ.get("GIPHY_API")
bot_id = None


RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
START_COMMAND = "GIPHY GIPHY GIPHYSNAP GO!"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

# Channel ID to run in
CHANNEL = os.environ.get("GIPHYSNAP_CHANNEL")


# Event types
INVOCATION = 1
COMMAND = 2


def number_of_words(string):
    """Return the number of words in a string.

    :param string: The string to check
    """
    return len(title.strip().split(" "))


def any_match(first_string, second_string):
    """Return whether two strings share a word.

    :param first_string: The first string to check
    :param second_string: The second string to check
    """
    if first_string is None or second_string is None:
        return False
    for first_word in first_string.strip().split(" "):
        for second_word in second_string.strip().split(" "):
            if first_word == second_word:
                return True
    return False


ILLEGAL_WORDS = [
    "taylor",
    "swift",
]


def illegal_words(string):
    """Return wether `string` contains an illegal word.

    :param string:
    """
    for word in string.strip().split(" "):
        if word.lower() in ILLEGAL_WORDS:
            return True
    return False


def read_slack_events(slack_events):
    """Return events GiphySnapBot is interested in from the event stream.

    :param slack_events: Slack events object.
    :return: A dict containing the event type and meta data.
    """
    for event in slack_events:
        if event.get("channel") == CHANNEL:
            if event["type"] == "message" and "subtype" not in event:
                user_id, message = parse_direct_mention(event["text"])
                if user_id == bot_id:
                    return {
                        "type": COMMAND,
                        "meta": {
                            "message": message
                        },
                    }

            attachments = event.get("attachments")
            if attachments is None:
                return

            footer = attachments[0].get("footer", "")
            if footer.startswith("Posted using /giphy"):
                if attachments is not None:
                    title = attachments[0].get("title")
                    url = attachments[0].get("title_link")
                    return {
                        "type": INVOCATION,
                        "meta": {
                            "title": title,
                            "url": url,
                        },
                    }


def parse_direct_mention(message_text):
    """Return a direction mention message."""
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the
    # remaining message
    empty = (None, None)
    return (matches.group(1), matches.group(2).strip()) if matches else empty


def handle_command(command):
    """Executes bot command if the command is known"""
    if command.startswith(START_COMMAND):
        # Create two random words
        term = "{} {}".format(r.get_random_word(), r.get_random_word())
        # Search giphy for those two words
        api_response = api_instance.gifs_search_get(api_key, term, limit=1)

        if len(api_response.data) > 0:
            # If it returned something, post the preview giph and title
            url = api_response.data[0].images.preview_gif.url
            attachment = {
                "title": term,
                "image_url": url,
                "title_link": url,
            }
            # Sends the response back to the channel
            slack_client.api_call(
                "chat.postMessage",
                channel=CHANNEL,
                attachments=[attachment],
            )
        else:
            # if it doesn't find anything, show an error
            slack_client.api_call(
                "chat.postMessage",
                channel=CHANNEL,
                message="couldn't find {}".format(term),
            )


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]

        previous_url = None
        previous_title = None
        while True:
            time.sleep(RTM_READ_DELAY)
            title, url = read_slack_events(slack_client.rtm_read())

            if title == starterbot_id:
                handle_command(url)
                continue

            if url is None or title is None:
                continue

            if title == previous_title:
                slack_client.api_call(
                    "chat.postMessage",
                    channel=CHANNEL,
                    text=("Infraction: You cannot use the same invocation "
                          "twice!"),
                )
                continue

            if number_of_words(title) != 2:
                slack_client.api_call(
                    "chat.postMessage",
                    channel=CHANNEL,
                    text="Infraction: You must invoke using two words!",
                )
                continue

            if any_match(previous_title, title):
                slack_client.api_call(
                    "chat.postMessage",
                    channel=CHANNEL,
                    text="Infraction: You cannot repeat a word!",
                )
                continue

            if illegal_words(title):
                slack_client.api_call(
                    "chat.postMessage",
                    channel=CHANNEL,
                    text="Infraction: You have used an illegal word!",
                )
                continue

            if url == previous_url:
                slack_client.api_call(
                    "chat.postMessage",
                    channel=CHANNEL,
                    text="Giphysnap!"
                )
            previous_title = title
            previous_url = url
    else:
        print("Connection failed. Exception traceback printed above.")
