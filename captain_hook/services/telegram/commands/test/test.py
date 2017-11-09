# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ..base import BaseCommand
from time import sleep


class TestCommand(BaseCommand):
    def get_description(self):
        return "Testing 1 2 3"

    def run(self, messageObj, config):
        self.send_message(
            chat_id=messageObj.get('chat').get('id'),
            text='Sleeping for 5s then saying: test')
        sleep(5)
        self.send_message(
            chat_id=messageObj.get('chat').get('id'),
            text='test')
