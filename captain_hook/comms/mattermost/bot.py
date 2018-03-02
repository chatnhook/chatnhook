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
            c = self.config['webhook_url'].split('/hooks/')
            self.mattermost_bot = Webhook(c[0], c[1])
            self.mattermost_bot.send(message, username=self.project_service_config['bot_name'])
