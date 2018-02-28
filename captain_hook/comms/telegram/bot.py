from __future__ import absolute_import
import telegram
from ..base.base_comm import BaseComm


class TelegramComm(BaseComm):
    def setup(self):
        print self.project_service_config
        if self.project_service_config.get('token', False):
            self.telegram_bot = telegram.Bot(self.project_service_config.get('token'))
        else:
            self.telegram_bot = telegram.Bot(self.config.get('token'))

    def communicate(self, message):
        if not message:
            return None
        self.telegram_bot.sendMessage(
            self.config["channel"],
            message,
            parse_mode=telegram.ParseMode.MARKDOWN
        )
