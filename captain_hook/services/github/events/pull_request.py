# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class PullRequestEvent(BaseEvent):

    def process(self):

        pr_link = str(self.body['pull_request']['url']).replace('https://api.github.com/', '')
        params = {
            'username': self.body['pull_request']['user']['login'],
            'user_link': self.body['pull_request']['user']['html_url'],
            'pull_request_number': str(self.body['pull_request']['number']),
            'pull_request_link': self.body['pull_request']['html_url'],
            'pull_request_title': self.body['pull_request']['title'],
            'body': str(self.body['pull_request']['body']).strip(),
            'repository_name': self.body['repository']['full_name'],
            'repository_link': self.body['repository']['html_url'],
        }
        message = False

        if self.body['action'] == 'opened':
            message = "[⛓]({pull_request_link}) [{username}]({user_link}) opened new pull request [#{pull_request_number} {pull_request_title}]({pull_request_link}) in [{repository_name}]({repository_link})"

        if self.body['action'] == 'closed' and self.body['pull_request']['merged'] == True:
            message = "[⛓]({pull_request_link}) [{username}]({user_link}) merged pull request [#{pull_request_number} {pull_request_title}]({pull_request_link})"

        if self.body['action'] == 'closed' and self.body['pull_request']['merged'] == False:
            message = "[⛓]({pull_request_link}) [{username}]({user_link}) closed pull request [#{pull_request_number} {pull_request_title}]({pull_request_link}) in [{repository_name}](repository_link)"

        message = message.format(**params)

        return {"telegram": str(message)}