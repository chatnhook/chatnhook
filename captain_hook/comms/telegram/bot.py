from __future__ import absolute_import
import telegram
from ..base.base_comm import BaseComm


class TelegramComm(BaseComm):

    def setup(self):
        self.bot = telegram.Bot(self.config["token"])

    def communicate(self, message):
        if not message:
            return None
        self.bot.sendMessage(
            self.config["channel"],
            message,
            parse_mode=telegram.ParseMode.MARKDOWN
        )
