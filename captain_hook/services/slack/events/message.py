# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class MessageEvent(BaseEvent):

    def process(self, request, body):
        if self.config['token'] != body.get('token'):
            return {'default': False}

        message = '[slack] {domain}:#{channel} <{user}>: {text}'.format(
            domain=body.get('team_domain', type=str),
            channel=body.get('channel_name', type=str),
            user=body.get('user_name', type=str),
            text=body.get('text', type=str)
        )

        return {"telegram": '\\' + message, "slack": message}
