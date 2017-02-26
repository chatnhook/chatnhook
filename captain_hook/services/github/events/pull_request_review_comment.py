# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class PullRequestReviewCommentEvent(BaseEvent):

    def process(self):
        params = {
            'username': self.body['comment']['user']['login'],
            'user_link': self.body['comment']['user']['html_url'],
            'pr_comment_link':  str(self.body['comment']['html_url']),
            'pr_number': str(self.body['pull_request']['number']),
            'pr_title': self.body['pull_request']['title'],
            'pr_link': self.body['pull_request']['html_url'],
        }

        message = False
        if self.body['action'] == 'created':
            message = "[🗨]({pr_comment_link}) [{username}]({user_link}) commented on a file in PR [#{pr_number} {pr_title}]({pr_link})"
            # message += '```{body}```'
            message = message.format(**params)

        if self.body['action'] == 'edited':
            message = "[🗨]({pr_comment_link}) [{username}]({user_link}) edited the comment on a file in PR [#{pr_number} {pr_title}]({pr_link})"
            # message += '```{body}```'
            message = message.format(**params)


        return {"telegram": str(message)}