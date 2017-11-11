# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class PushEvent(BaseEvent):
    def process(self, request, body):
        repo = body.get('repository', {}).get('repo_name', '')
        tag = body.get('push_data', {}).get('tag', '')
        if tag:
            tag = ':' + tag

        message = '[🐳] Docker image {repo}:{tag} updated'.format(
            tag=tag, repo=repo)
        return {"default": str(message)}
