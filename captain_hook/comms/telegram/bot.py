from __future__ import absolute_import
import telegram
from ..base.base_comm import BaseComm


class TelegramComm(BaseComm):
    def setup(self):
        if self.project_service_config.get('token', False):
            self.telegram_bot = telegram.Bot(self.project_service_config.get('token'))
        else:
            self.telegram_bot = telegram.Bot(self.config.get('token'))

    def communicate(self, message):
        if not message:
            return None

        channels = self.project_service_config.get('channels')
        if channels:
            for channel in channels:
                self.telegram_bot.sendMessage(
                    channel,
                    message,
                    parse_mode=telegram.ParseMode.MARKDOWN
                )
        else:
            self.telegram_bot.sendMessage(
                self.config["channel"],
                message,
                parse_mode=telegram.ParseMode.MARKDOWN
            )
