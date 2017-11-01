# -*- coding: utf-8 -*-
from __future__ import absolute_import
import telegram


class BaseCommand:
    def __init__(self, config):
        self.config = config
        self.telegram_bot = telegram.Bot(self.config["token"])

    def run(self, messageObj, config):
        raise NotImplementedError

    def sendMessage(self, chat_id,
                    text,
                    parse_mode=telegram.ParseMode.MARKDOWN,
                    disable_web_page_preview=None,
                    disable_notification=False,
                    reply_to_message_id=None,
                    reply_markup=None,
                    timeout=None,
                    **kwargs):
        self.telegram_bot.sendMessage(chat_id,
                                      text,
                                      parse_mode,
                                      disable_web_page_preview,
                                      disable_notification,
                                      reply_to_message_id,
                                      reply_markup,
                                      timeout,
                                      **kwargs
                                      )
        # parse_mode=
