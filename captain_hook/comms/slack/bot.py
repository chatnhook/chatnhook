from __future__ import absolute_import
import slackweb
from ..base.base_comm import BaseComm


class SlackComm(BaseComm):

    def setup(self):
        self.slack_bot = slackweb.Slack(url=self.config["hook_url"])

    def communicate(self, message):
        if not message:
            return None
        self.slack_bot.notify(text=message)

        #     sendMessage(
        #     self.config["channel"],
        #     message,
        #     parse_mode=telegram.ParseMode.MARKDOWN
        # )
