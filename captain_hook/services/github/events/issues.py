# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class IssuesEvent(BaseEvent):

    def process(self, request, body):
        params = {
            'username': body['sender']['login'],
            'user_link': body['sender']['html_url'],
            'issue_number': str(body['issue']['number']),
            'issue_link':  body['issue']['html_url'],
            'issue_title': body['issue']['title'],
            'body': body['issue']['body'],
            'repository_name': body['repository']['full_name'],
            'repository_link': body['repository']['html_url'],
        }
        message = False
        if body['action'] == 'opened':
            message = "[❓]({issue_link}) [{username}]({user_link}) opened new issue [#{issue_number} {issue_title}]({issue_link}) in [{repository_name}]({repository_link})"

        if body['action'] == 'closed':
            message = "[❓]({issue_link}) [{username}]({user_link}) closed issue [#{issue_number} {issue_title}]({issue_link}) in [{repository_name}]({repository_link})"

        message = message.format(**params)

        return {"default": str(message)}
