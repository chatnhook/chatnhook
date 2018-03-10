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
        else:
            self.discord_bot = DiscordWebhook(url=self.config.get('hook_url'))
            self.discord_bot.notify(text=message,
                                    username=self.config.get('bot_name'))
    def get_comm_config_model(self):
        return [
            {
                'name': 'hook_url',
                'label': 'Webhook URL',
                'type': 'text',
                'description': ''
            },
            {
                'name': 'bot_name',
                'label': 'Bot name',
                'type': 'text',
                'description': 'If the project doesn\'t has a bot name configured.<br />This name will be used'
            },
        ]