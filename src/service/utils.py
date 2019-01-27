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


def is_invocation(event):
    """Return whether the event is an invocation."""
    attachments = event.get("attachments")
    if attachments is None or len(attachments) < 1:
        return False

    footer = attachments[0].get("footer", "")
    if footer.startswith("Posted using /giphy"):
        return True

    return False


def parse_invocation(event):
    """Return the term and url for the invocation.

    The term is used to check against rules. And the URL is used to check a
    winner.
    """
    attachments = event.get("attachments")
    title = attachments[0].get("title")
    url = attachments[0].get("title_link")

    return title, url
