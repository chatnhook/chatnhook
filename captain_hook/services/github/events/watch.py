# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class WatchEvent(BaseEvent):
    def process(self, request, body):
        user_link = body['sender']['html_url'].replace('https://github.com/', '')
        repo_link = body['repository']['html_url'].replace('https://github.com/', '')

        params = {
            'username': body['sender']['login'],
            'user_link': body['sender']['html_url'],
            'repository_name': body['repository']['full_name'],
            'repository_link': body['repository']['html_url'],
        }
        message = False
        if body['action'] == 'started':
            message = "❤ [{username}]({user_link}) starred [{repository_name}]({repository_link})"
            message = message.format(**params)

        return {"default": str(message)}
