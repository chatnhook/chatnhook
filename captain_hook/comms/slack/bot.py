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