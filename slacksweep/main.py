# -*- coding: utf-8 -*-
# Copyright © 2021, RMK HAKLAB RY
"""slack sweeper main program
"""
import datetime
import logging
import os
import sys
import time

from .slack import SlackChannel


_log = logging.getLogger(__name__)


def main():
    """Query slack channel for messages that are older than two
    weeks and delete them in accordance to the privacy policy
    set for the automatic monitoring.

    Raises:
        ValueError: when missing the required environment variables
    """
    token = os.environ.get("SLACK_BOT_TOKEN")
    if not token:
        raise ValueError("No SLACK_BOT_TOKEN defined")
    channel = os.environ.get("SLACK_CHANNEL")
    if not channel:
        raise ValueError("No SLACK_CHANNEL defined")
    bot_id = os.environ.get("SLACKBOT_ID")
    if not bot_id:
        raise ValueError("No SLACKBOT_ID defined")

    try:
        upto = sys.argv[1]
    except IndexError:
        upto = "14 days ago"

    slack_channel = SlackChannel(token=token, channel=channel)

    # Get all the messages older than two weeks and delete them
    # one by one, this is rate limited so wait for one second
    # after each delete
    for msg in list(slack_channel.messages(upto=upto)):
        # Do not try to delete messages that are not created by the bot
        if msg.get("bot_id") != bot_id:
            continue
        message_id = msg["ts"]
        msg_time = datetime.datetime.fromtimestamp(
            float(message_id)).isoformat()
        if not slack_channel.delete_message(message_id=message_id):
            _log.error("Failed to delete message %s", msg_time)
            continue
        _log.info("Deleted message %s", msg_time)
        time.sleep(1.0)
