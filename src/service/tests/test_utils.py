"""Tests for service.utils."""
import unittest

from service.utils import (
    is_direct_mention,
    parse_direct_mention,
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
