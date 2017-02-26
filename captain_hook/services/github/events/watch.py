# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class WatchEvent(BaseEvent):
    def process(self):
        user_link = self.body['sender']['html_url'].replace('https://github.com/', '')
        repo_link = self.body['repository']['html_url'].replace('https://github.com/', '')

        params = {
            'username': self.body['sender']['login'],
            'user_link': self.body['sender']['html_url'],
            'repository_name': self.body['repository']['full_name'],
            'repository_link': self.body['repository']['html_url'],
        }
        message = False
        if self.body['action'] == 'started':
            message = "❤ [{username}]({user_link}) starred [{repository_name}]({repository_link})"
            message = message.format(**params)

        return {"default": str(message)}
