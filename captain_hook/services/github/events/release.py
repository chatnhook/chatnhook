# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class ReleaseEvent(BaseEvent):
    def process(self):
        params = {
            'username': self.body['sender']['login'],
            'user_link': self.body['sender']['html_url'],
            'tag': self.body['release']['tag_name'],
            'tag_link': self.body['release']['html_url'],
            'repository_name': self.body['repository']['full_name'],
            'repository_link': self.body['repository']['html_url'],
        }
        message = False
        if self.body['action'] == 'published':
            message = "🚀 [{username}]({user_link}) added tag [{tag}]({tag_link}) to [{repository_name}]({repository_link})"
            message = message.format(**params)

        return {"default": str(message)}
