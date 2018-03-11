from __future__ import absolute_import
import slackweb
from ..base.base_comm import BaseComm


class SlackComm(BaseComm):
    def setup(self):
        pass

    def communicate(self, message):
        if not message:
            return None
        hooks = self.project_service_config.get('webhooks')
        if hooks:
            for hook in hooks:
                self.slack_bot = slackweb.Slack(url=hook)
                self.slack_bot.notify(text=message,
                                      username=self.project_service_config.get('bot_name', ''))

        else:
            self.slack_bot = slackweb.Slack(url=self.config.get('hook_url'))
            self.slack_bot.notify(text=message,
                                  username=self.config.get('bot_name'))
    def get_comm_config_model(self):
        return [
            {
                'name': 'hook_url',
                'label': 'Webhook URL',
                'type': 'text',
                'description': ''
            },
        ]

    def get_comm_project_config_model(self):
        return [
            {
                'name': 'enabled',
                'label': 'Enabled',
                'type': 'checkbox',
                'description': ''
            },
            {
                'name': 'bot_name',
                'label': 'Bot name',
                'type': 'text',
                'description': 'If the project doesn\'t has channels configured<br />it will be send to this channel'
            },
            {
                'name': 'webhooks',
                'label': 'Webhooks',
                'type': 'array',
                'description': ''
            },
        ]
