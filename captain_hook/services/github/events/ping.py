# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class PingEvent(BaseEvent):

    def process(self, request, body):
        params = {
            'repo': body['repository']['full_name']
        }

        message = "Webhook works for: {repo}".format(**params)

        return {"default": str(message)}
