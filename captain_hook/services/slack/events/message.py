# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class MessageEvent(BaseEvent):
    def process(self):
        if self.config['token'] != self.body.get('token'):
            return False

        message = '[slack] {domain}:#{channel} <{user}>: {text}'.format(
            domain=self.body.get('domain', type=str),
            channel=self.body.get('channel_name', type=str),
            user=self.body.get('user_name', type=str),
            text=self.body.get('text', type=str)
        )

        return {"telegram": '\\'+message, "slack": message}
