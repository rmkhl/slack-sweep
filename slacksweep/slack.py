# -*- coding: utf-8 -*-
# Copyright © 2021, RMK HAKLAB RY
"""Interface to the slack api for channel
"""
import logging

from typing import Iterable

from dateparser import parse
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


_log = logging.getLogger(__name__)


class SlackChannel:
    """Abstraction of slack channel API
    """
    def __init__(self, *, token: str, channel: str):
        self._client = WebClient(token=token)
        self._channel = channel
        self._msgs = None

    def _load_conversation(self, *, latest: float) -> Iterable:
        cursor = None
        while True:
            try:
                response = self._client.conversations_history(
                    channel=self._channel,
                    latest=latest,
                    cursor=cursor,
                )
                if response.status_code != 200:
                    _log.error("%r", response)
                    return
                if not response.data.get("ok", False):
                    _log.error("%s", response.data.get(
                        "error", "unknown failure"))
                    return
                for msg in response.data.get("messages", []):
                    yield msg

                if not response.data.get("has_more", False):
                    return

                cursor = response.data.get(
                    "response_metadata", {}).get("next_cursor")

            except SlackApiError:
                _log.exception("Failed to retrieve conversation messages")
                return

    def messages(self, *, upto: str) -> Iterable:
        """Yield all messages in the channel upto given time
        """
        yield from self._load_conversation(latest=parse(upto).timestamp())

    def delete_message(self, *, message_id: str) -> bool:
        """Delete specific message from the chat
        """
        try:
            response = self._client.chat_delete(
                channel=self._channel, ts=message_id)
            return response.status_code == 200
        except SlackApiError:
            _log.exception("Failed to delete message")
        return False
