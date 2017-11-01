# -*- coding: utf-8 -*-
from __future__ import absolute_import
from captain_hook.services.telegram.commands.base import BaseCommand
from time import sleep


class TestCommand(BaseCommand):
    def run(self, messageObj, config):
        self.sendMessage(chat_id=messageObj.get('chat').get('id'),
                         text='Sleeping for 5s then saying: test')
        sleep(5)
        self.sendMessage(chat_id=messageObj.get('chat').get('id'),
                         text='test')
