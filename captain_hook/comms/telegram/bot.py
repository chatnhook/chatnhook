import telegram
from ..base.base_comm import BaseComm


class TelegramComm(BaseComm):

    def setup(self):
        self.bot = telegram.Bot(self.config["token"])

    def communicate(self, message):
        self.bot.sendMessage(
            chat_id=self.config["channel"],
            text=message,
            parse_mode=telegram.ParseMode.HTML
        )
