from __future__ import absolute_import
import telegram
from ..base.base_comm import BaseComm


class TelegramComm(BaseComm):
    def setup(self):
        self.telegram_bot = telegram.Bot(self.config["token"])

    def communicate(self, message):
        if not message:
            return None
        self.telegram_bot.sendMessage(
            self.config["channel"],
            message,
            parse_mode=telegram.ParseMode.MARKDOWN
        )
