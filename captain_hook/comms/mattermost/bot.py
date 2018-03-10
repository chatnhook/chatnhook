from __future__ import absolute_import
from matterhook import Webhook
from ..base.base_comm import BaseComm


class MattermostComm(BaseComm):
    def setup(self):
        pass

    def communicate(self, message):
        if not message:
            return None

        hooks = self.project_service_config.get('webhooks')
        if hooks:
            for hook in hooks:
                c = hook.split('/hooks/')
                self.mattermost_bot = Webhook(c[0], c[1])
                self.mattermost_bot.send(message, username=self.config['bot_name'])

        else:
            c = self.config['hook_url'].split('/hooks/')
            self.mattermost_bot = Webhook(c[0], c[1])
            self.mattermost_bot.send(message, username=self.project_service_config['bot_name'])

    def get_comm_config_model(self):
        return [
            {
                'name': 'webhook_url',
                'label': 'Webhook URL',
                'type': 'text',
                'description': ''
            },
            {
                'name': 'channel',
                'label': 'Channel',
                'type': 'text',
                'description': 'If the project doesn\'t has channels configured.<br />it will be send to this channel'
            },
            {
                'name': 'bot_name',
                'label': 'Bot name',
                'type': 'text',
                'description': 'If the project doesn\'t has a bot name configured.<br />This name will be used'
            },
        ]