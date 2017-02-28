from __future__ import absolute_import
from matterhook import Webhook
from ..base.base_comm import BaseComm


class MattermostComm(BaseComm):

    def setup(self):
        c = self.config['webhook_url'].split('/hooks/')
        self.mattermost_bot = Webhook(c[0], c[1])

    def communicate(self, message):
        if not message:
            return None
        self.mattermost_bot.send(message, channel=self.config[
                                 'channel'], username=self.config['bot_name'])
