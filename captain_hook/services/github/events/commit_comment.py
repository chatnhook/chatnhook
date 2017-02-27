# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class CommitCommentEvent(BaseEvent):

    def process(self, request, body):
        params = {
            'username': body['comment']['user']['login'],
            'user_link': body['comment']['user']['html_url'],
            'commit_hash': str(body['comment']['commit_id'])[:7],
            'commit_comment_link': body['comment']['html_url'],
            'body': str(body['comment']['body']).split("\n")[0],
        }

        message = False
        if body['action'] == 'created':
            message = "[🗨]({commit_comment_link}) [{username}]({user_link}) commented on [{commit_hash}]({commit_comment_link})"
            # message += '```{body}```'
            message = message.format(**params)

        if body['action'] == 'edited':
            message = "[🗨]({commit_comment_link}) [{username}]({user_link}) edited the comment on [{commit_hash}]({commit_comment_link})"
            # message += '```{body}```'
            message = message.format(**params)

        return {"default": str(message)}
