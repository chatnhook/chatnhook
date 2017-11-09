# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import GithubEvent


class PingEvent(GithubEvent):
    def process(self, request, body):
        params = {
            'repo': body['repository']['full_name']
        }

        message = "Webhook works for: {repo}".format(**params)

        return {"default": str(message)}
