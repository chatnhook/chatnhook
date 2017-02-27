# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class PullRequestReviewCommentEvent(BaseEvent):

    def process(self, request, body):
        params = {
            'username': body['comment']['user']['login'],
            'user_link': body['comment']['user']['html_url'],
            'pr_comment_link':  str(body['comment']['html_url']),
            'pr_number': str(body['pull_request']['number']),
            'pr_title': body['pull_request']['title'],
            'pr_link': body['pull_request']['html_url'],
        }

        message = False
        if body['action'] == 'created':
            message = "[🗨]({pr_comment_link}) [{username}]({user_link}) commented on a file in PR [#{pr_number} {pr_title}]({pr_link})"
            # message += '```{body}```'
            message = message.format(**params)

        if body['action'] == 'edited':
            message = "[🗨]({pr_comment_link}) [{username}]({user_link}) edited the comment on a file in PR [#{pr_number} {pr_title}]({pr_link})"
            # message += '```{body}```'
            message = message.format(**params)


        return {"default": str(message)}
