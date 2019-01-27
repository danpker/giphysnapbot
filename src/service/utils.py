"""Utility functions for giphysnap."""
import re


MENTION_REGEX = re.compile("^<@(|[WU].+?)>(.*)")


def is_direct_mention(message_text):
    """Return whether the message is a direct mention."""
    if MENTION_REGEX.match(message_text) is not None:
        return True
    return False


def parse_direct_mention(message_text):
    """Return a direction mention message."""
    matches = re.match(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the
    # remaining message
    empty = (None, None)
    return (matches.group(1), matches.group(2).strip()) if matches else empty
