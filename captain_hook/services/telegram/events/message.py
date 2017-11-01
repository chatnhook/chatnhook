# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent
from pprint import pprint

class MessageEvent(BaseEvent):
    def process(self, request, body):
        print('Telegram webhook')
        update = body

        if update.get('message').get('text') == 'ping':
            return {"telegram": str('Pong!')}
        else:
            return {"telegram": str('Pong!')}
