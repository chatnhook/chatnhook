# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ..base import BaseCommand
import random
from pprint import pprint


class RandomCommand(BaseCommand):
    def get_description(self):
        return "Pick something for you"

    def run(self, messageObj, config):
        message = ' '.join(messageObj.get('args'))
        pprint(message)
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

        self.send_message(chat_id=messageObj.get('chat').get('id'),
                          text=msg.format())
