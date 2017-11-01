# -*- coding: utf-8 -*-
from __future__ import absolute_import
import telegram


class BaseCommand:
    def __init__(self, config):
        self.config = config
        self.telegram_bot = telegram.Bot(self.config["token"])

    def run(self, message, config):
        raise NotImplementedError

    def sendMessage(self, receiver, text):
        self.telegram_bot.sendMessage(
            receiver,
            text,
            parse_mode=telegram.ParseMode.MARKDOWN
        )
