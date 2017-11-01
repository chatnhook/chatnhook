# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent
from pprint import pprint
import json
class MessageEvent(BaseEvent):
    def process(self, request, body):
        print('Telegram webhook')
        update = body
        print json.dumps(body)
        if update.get('message', '') and update.get('message').get('text') == 'ping':
            return {"telegram": str('Pong!')}
        else:
            return {"telegram": str('')}
