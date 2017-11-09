from __future__ import absolute_import
from ..base.base_comm import BaseComm

from .discordWebhooks import DiscordWebhook


class DiscordComm(BaseComm):
    def setup(self):
        self.discord_bot = DiscordWebhook(url=self.config["hook_url"])

    def communicate(self, message):
        if not message:
            return None
        message = 'test'
        self.discord_bot.notify(text=message, username=self.config['bot_name'])

        #     sendMessage(
        #     self.config["channel"],
        #     message,
        #     parse_mode=telegram.ParseMode.MARKDOWN
        # )
