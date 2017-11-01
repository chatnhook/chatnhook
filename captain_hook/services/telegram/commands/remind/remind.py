# -*- coding: utf-8 -*-
from __future__ import absolute_import
from captain_hook.services.telegram.commands.base import BaseCommand
from pprint import pprint


class RemindCommand(BaseCommand):
    def run(self, message, config):
        self.sendMessage(message.get('chat').get('id'), 'remind')
