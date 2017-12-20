# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ....commands.base import BaseCommand


class PingService(BaseCommand):
    def run(self, messageObj, config):
        if messageObj.get('text', '') == 'ping':
            self.send_message(
                chat_id=messageObj.get('chat').get('id'),
                text='Pong!')
