# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class IssueEvent(BaseEvent):
    def process(self, request, body):
        message = body['payload']
        return {"default": message}
