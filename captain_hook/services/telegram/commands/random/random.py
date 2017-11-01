# -*- coding: utf-8 -*-
from __future__ import absolute_import
from captain_hook.services.telegram.commands.base import BaseCommand
from time import sleep
import random
from pprint import pprint


class RandomCommand(BaseCommand):
    def run(self, messageObj, config):
        pprint(messageObj)
        message = ' '.join(messageObj.get('args'))
        usage = 'Usage: /random answer1, answer2, answer 3'
        if not message or message == '':
            msg = usage
        else:
            answers = message.split(',')
            if len(answers) == 1 or len(answers) == 0:
                msg = usage
            else:
                answer = random.choice(answers)
                msg = 'You rolled: ' + answer

        self.sendMessage(chat_id=messageObj.get('chat').get('id'),
                         text=msg.format())
