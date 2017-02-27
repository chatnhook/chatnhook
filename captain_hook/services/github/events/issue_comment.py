# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class IssueCommentEvent(BaseEvent):

    def process(self, request, body):
        issue_type = 'issue'
        if 'pull_request' in body['issue']:
            issue_type = 'pull request'
        params = {
            'username': body['comment']['user']['login'],
            'user_link': body['comment']['user']['html_url'],
            'issue_number': str(body['issue']['number']),
            'comment_link': body['comment']['html_url'],
            'issue_title': body['issue']['title'],
            'issue_type': issue_type,
            'body': str(body['comment']['body']).split("\n")[0] + '...',
        }

        if body['action'] == 'created':
            message = "[🗨]({comment_link}) [{username}]({user_link}) commented on {issue_type} [#{issue_number} {issue_title}]({comment_link})"
            # message += '```{body}```'
            message = message.format(**params)

        if body['action'] == 'edited':
            message = "[🗨]({comment_link}) [{username}]({user_link}) edited the comment on {issue_type} [#{issue_number} {issue_title}]({comment_link})"
            # message += '```{body}```'
            message = message.format(**params)

        return {"default": str(message)}
