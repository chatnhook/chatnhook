# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent
import telegram
import json
class MessageEvent(BaseEvent):

    def process(self):
        print('Telegram webhook')
        update = self.request.get_json(force=True)
        print update
        message = 'For a private message from: {username}: {message}'.format(
            username=update['message']['from']['username'],
            message=update['message']['text'],
        )
        return {"telegram": str('')}