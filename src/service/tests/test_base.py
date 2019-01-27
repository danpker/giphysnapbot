"""Tests for service.GiphySnapBot."""
import unittest
from unittest.mock import (
    MagicMock,
    patch,
)

import pytest
from slackclient import SlackClient

from service import base
from service.base import GiphySnapBotBase


TEST_CONFIG = {
    "slack_bot_token": "baby shark",
}


class GiphySnapBotBaseTestCase(unittest.TestCase):
    """Tests for GiphySnapBotBase."""

    @patch.object(
        base.SlackClient, "rtm_connect", return_value={"ok": True})
    @patch.object(GiphySnapBotBase, "_get_user_id")
    def test_connect_will_return_slack_client(self, *args):
        """If Slack connection is ok, _connect() will return the client."""
        client = GiphySnapBotBase(TEST_CONFIG)
        self.assertEqual(client._slack_client.__class__, SlackClient)

    @patch.object(
        base.SlackClient, "rtm_connect", return_value={"error": "foo"})
    def test_connection_error_will_raise_connection_error(self, *args):
        """If rtm_connect() fails, raise a ConnectionError."""
        with pytest.raises(ConnectionError):
            GiphySnapBotBase(TEST_CONFIG)

    @patch.object(GiphySnapBotBase, "_connect", return_value=MagicMock())
    def test_get_user_id_will_return_user_id(self, mock_client):
        """_get_user_id() will return the user of the bot."""
        mock_client.return_value.api_call = MagicMock(
            return_value={"ok": True, "user_id": "mort"})
        client = GiphySnapBotBase(TEST_CONFIG)

        self.assertEqual(client._bot_id, "mort")

    @patch.object(GiphySnapBotBase, "_connect", return_value=MagicMock())
    def test_get_user_id_will_raise_permission_error_if_response_not_ok(
            self, mock_client):
        """_get_user_id() will raise a PermissionError if response not ok."""
        mock_client.return_value.api_call = MagicMock(
            return_value={"ok": False, "error": "abc123"})

        with pytest.raises(PermissionError):
            GiphySnapBotBase(TEST_CONFIG)

    @patch.object(GiphySnapBotBase, "_connect", return_value=MagicMock())
    def test_send_messge_will_send_post_message_api_call(self, mock_client):
        """send_message() will send message using postMessage api call."""
        # Get the right mock for client
        mock_client = mock_client.return_value
        client = GiphySnapBotBase(TEST_CONFIG)
        mock_client.reset_mock()

        client.send_message("foo_channel", "bar_message")

        mock_client.api_call.assert_called_once()
