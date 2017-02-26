# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class CommitCommentEvent(BaseEvent):

    def process(self):
        params = {
            'username': self.body['comment']['user']['login'],
            'user_link': self.body['comment']['user']['html_url'],
            'commit_hash': str(self.body['comment']['commit_id'])[:7],
            'commit_comment_link': self.body['comment']['html_url'],
            'body': str(self.body['comment']['body']).split("\n")[0],
        }

        message = False
        if self.body['action'] == 'created':
            message = "[🗨]({commit_comment_link}) [{username}]({user_link}) commented on [{commit_hash}]({commit_comment_link})"
            # message += '```{body}```'
            message = message.format(**params)

        if self.body['action'] == 'edited':
            message = "[🗨]({commit_comment_link}) [{username}]({user_link}) edited the comment on [{commit_hash}]({commit_comment_link})"
            # message += '```{body}```'
            message = message.format(**params)

        return {"telegram": str(message)}