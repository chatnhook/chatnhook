# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class IssueCommentEvent(BaseEvent):

    def process(self):
        issue_type = 'issue'
        if 'pull_request' in self.body['issue']:
            issue_type = 'pull request'
        params = {
            'username': self.body['comment']['user']['login'],
            'user_link': self.body['comment']['user']['html_url'],
            'issue_number': str(self.body['issue']['number']),
            'comment_link': self.body['comment']['html_url'],
            'issue_title': self.body['issue']['title'],
            'issue_type': issue_type,
            'body': str(self.body['comment']['body']).split("\n")[0] + '...',
        }

        if self.body['action'] == 'created':
            message = "[🗨]({comment_link}) [{username}]({user_link}) commented on {issue_type} [#{issue_number} {issue_title}]({comment_link})"
            # message += '```{body}```'
            message = message.format(**params)

        if self.body['action'] == 'edited':
            message = "[🗨]({comment_link}) [{username}]({user_link}) edited the comment on {issue_type} [#{issue_number} {issue_title}]({comment_link})"
            # message += '```{body}```'
            message = message.format(**params)

        return {"default": str(message)}
