# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class IssuesEvent(BaseEvent):

    def process(self):
        params = {
            'username': self.body['sender']['login'],
            'user_link': self.body['sender']['html_url'],
            'issue_number': str(self.body['issue']['number']),
            'issue_link':  self.body['issue']['html_url'],
            'issue_title': self.body['issue']['title'],
            'body': self.body['issue']['body'],
            'repository_name': self.body['repository']['full_name'],
            'repository_link': self.body['repository']['html_url'],
        }
        message = False
        if self.body['action'] == 'opened':
            message = "[❓]({issue_link}) [{username}]({user_link}) opened new issue [#{issue_number} {issue_title}]({issue_link}) in [{repository_name}]({repository_link})"

        if self.body['action'] == 'closed':
            message = "[❓]({issue_link}) [{username}]({user_link}) closed issue [#{issue_number} {issue_title}]({issue_link}) in [{repository_name}]({repository_link})"

        message = message.format(**params)

        return {"telegram": str(message)}