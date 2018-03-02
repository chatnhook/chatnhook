from __future__ import absolute_import
from ..base.base_comm import BaseComm

from .discordWebhooks import DiscordWebhook


class DiscordComm(BaseComm):
    def setup(self):
        return

    def communicate(self, message):
        if not message:
            return None

        hooks = self.project_service_config.get('webhooks')
        if hooks:
            for hook in hooks:
                self.discord_bot = DiscordWebhook(url=hook)
                self.discord_bot.notify(text=message,
                                        username=self.project_service_config['bot_name'])
        #     sendMessage(
        #     self.config["channel"],
        #     message,
        #     parse_mode=telegram.ParseMode.MARKDOWN
        # )
