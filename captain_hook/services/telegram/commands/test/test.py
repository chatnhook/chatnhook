# -*- coding: utf-8 -*-
from __future__ import absolute_import
from captain_hook.services.telegram.commands.base import BaseCommand
from time import sleep


class TestCommand(BaseCommand):
    def run(self, message, config):
        sleep(5)
        self.sendMessage(message.get('chat').get('id'), 'test')
