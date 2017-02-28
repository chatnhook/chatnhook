# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent
import telegram
import json


class EditedMessageEvent(BaseEvent):

    def process(self, request, body):
        print('Telegram webhook')
        update = request.get_json(force=True)
        print update
        message = 'Edited private message from: {username}: {message}'.format(
            username=update['edited_message']['from']['username'],
            message=update['edited_message']['text'],
        )
        return {"telegram": str('')}
