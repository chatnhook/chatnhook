# -*- coding: utf-8 -*-
from __future__ import absolute_import
import telegram


class BaseCommand:
    def __init__(self, config):
        self.config = config
        self.telegram_bot = telegram.Bot(self.config["token"])
        self.bot_info = self.telegram_bot.getMe()

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
        try:
            self.telegram_bot.sendMessage(
                chat_id,
                text,
                parse_mode,
                disable_web_page_preview,
                disable_notification,
                reply_to_message_id,
                reply_markup,
                timeout,
                **kwargs
            )
        except telegram.error.RetryAfter:
            pass

    def sendPhoto(self, chat_id,
                  photo='',
                  **kwargs):
        try:
            self.telegram_bot.send_photo(chat_id=chat_id, photo=photo, **kwargs)
        except telegram.error.RetryAfter:
            pass

    def sendDocument(self, chat_id,
                     document='',
                     **kwargs):
        try:
            self.telegram_bot.send_document(chat_id=chat_id, document=document, **kwargs)
        except telegram.error.RetryAfter:
            pass
