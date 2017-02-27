# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class ReleaseEvent(BaseEvent):
    def process(self, request, body):
        params = {
            'username': body['sender']['login'],
            'user_link': body['sender']['html_url'],
            'tag': body['release']['tag_name'],
            'tag_link': body['release']['html_url'],
            'repository_name': body['repository']['full_name'],
            'repository_link': body['repository']['html_url'],
        }
        message = False
        if body['action'] == 'published':
            message = "🚀 [{username}]({user_link}) added tag [{tag}]({tag_link}) to [{repository_name}]({repository_link})"
            message = message.format(**params)

        return {"default": str(message)}
