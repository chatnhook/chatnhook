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

    def is_admin(self, username):
        return username in self.config.get('permissions', {}).get('admins')

    def is_moderator(self, username):
        return username in self.config.get('permissions', {}).get('moderators')

    def get_rank(self, username):
        if self.is_admin(username):
            return 'admin'
        if self.is_moderator(username):
            return 'moderator'
        return 'user'

    def send_message(self, chat_id,
                     text,
                     parse_mode=telegram.ParseMode.MARKDOWN,
                     disable_web_page_preview=None,
                     disable_notification=False,
                     reply_to_message_id=None,
                     reply_markup=None,
                     timeout=None,
                     **kwargs):
        try:
            self.telegram_bot.send_message(
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

    def send_photo(self, chat_id,
                   photo='',
                   **kwargs):
        try:
            self.telegram_bot.send_photo(chat_id=chat_id, photo=photo, **kwargs)
        except telegram.error.RetryAfter:
            pass

    def send_document(self, chat_id,
                      document='',
                      **kwargs):
        try:
            self.telegram_bot.send_document(chat_id=chat_id, document=document, **kwargs)
        except telegram.error.RetryAfter:
            pass

    def command_template(self):
        return []
