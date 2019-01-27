"""Tests for service.utils."""
import unittest

from service.utils import (
    is_direct_mention,
    is_invocation,
    parse_direct_mention,
    parse_invocation,
)


class IsDirectMentionTestCase(unittest.TestCase):
    """Tests for is_direct_mention()."""

    def test_will_return_true_for_direct_mention(self):
        """is_direct_mention() will return True for direct mention."""
        self.assertTrue(is_direct_mention("<@U1231>hello"))

    def test_will_return_false_is_not_direct_mention(self):
        """is_direct_mention() will return True for direct mention."""
        self.assertFalse(is_direct_mention("hello"))


class ParseDirectMentionTestCase(unittest.TestCase):
    """Tests for parse_direct_mention()."""

    def test_will_return_username_of_direct_mention(self):
        """parse_direct_mention() will return the username in the mention."""
        username, _ = parse_direct_mention("<@U1234>hello")
        self.assertEqual(username, "U1234")

    def test_will_return_message_for_direct_mention(self):
        """parse_direct_mention() will return the message in the mention."""
        _, message = parse_direct_mention("<@U1234>howdy")
        self.assertEqual(message, "howdy")


class IsInvocationTestCase(unittest.TestCase):
    """Tests for is_invocation()."""

    def test_will_return_true_for_giphy_result(self):
        """Will return True if the event was a giphy command."""
        event = {
            "attachments": [
                {
                    "footer": "Posted using /giphy"
                }
            ]
        }

        self.assertTrue(is_invocation(event))

    def test_will_return_false_for_no_attachments(self):
        """Will return false if event has no attachments."""
        event = {}
        self.assertFalse(is_invocation(event))
        event = {"attachments": []}
        self.assertFalse(is_invocation(event))

    def test_will_return_false_if_not_posted_using_gipht(self):
        """Will return False if the event was not crated by /giphy command."""
        event = {
            "attachments": [
                {"footer": "foo bar"}
            ]
        }
        self.assertFalse(is_invocation(event))

    def test_will_return_true_if_contains_gif_by_footer(self):
        """Will return true if the footer has "GIF by" text."""
        event = {
            "attachments": [
                {"footer": "Posted using /giphy | GIF by BBC"},
            ]
        }
        self.assertTrue(is_invocation(event))


class ParseInvocationTestCase(unittest.TestCase):
    """Tests for parse_invocation()."""

    def test_will_return_the_title_of_event(self):
        """Will return the title of the giphy response."""
        event = {
            "attachments": [
                {"title": "foo bar"},
            ]
        }

        title, _ = parse_invocation(event)
        self.assertEqual(title, "foo bar")

    def test_will_return_the_url_of_event(self):
        """Will return the url of the giphy response."""
        event = {
            "attachments": [
                {"title_link": "www.gif.com/gif"},
            ]
        }

        _, url = parse_invocation(event)
        self.assertEqual(url, "www.gif.com/gif")
