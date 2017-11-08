# -*- coding: utf-8 -*-
from __future__ import absolute_import
from captain_hook.services.telegram.commands.base import BaseCommand
from pprint import pprint
from threading import Timer
import re


def sendReminder(bot, message, reminder):
    msg = 'Hey {user_name}, this is a reminder for:\n' + reminder
    bot.sendMessage(chat_id=message.get('chat').get('id'),
                    text=msg.format(
                        user_name=message.get('from').get('first_name')))


class RemindCommand(BaseCommand):
    def get_description(self):
        return "The bot will remind you of something"

    def run(self, messageObj, config):
        message = messageObj.get('text')[1:]
        # message = ' '.join(message)
        regex = "(([0-9]+d)?([0-9]+h)?\s?([0-9]+m)?([0-9]+s)?)+$"
        matches = re.findall(regex, message)[0]
        reminder = re.sub(regex, '', message)
        modifiers = {
            'd': {
                'amount': 86400,
                'name': 'day'
            },
            'h': {
                'amount': 3600,
                'name': 'hour'
            },
            'm': {
                'amount': 60,
                'name': 'minute'
            },
            's': {
                'amount': 1,
                'name': 'second'
            }
        }
        matched = []
        total_seconds = 0
        for match in matches:
            amount = match[:-1]
            multiplier = match[-1:]
            if multiplier:
                total_seconds += (int(amount) * int(modifiers[multiplier]['amount']))
                plural = modifiers[multiplier]['name'] if int(amount) == 1 else modifiers[multiplier]['name'] + 's'
                matched.append('{amount} {plural}'.format(amount=amount, plural=plural))

        if matched:
            reminder_time = ', '.join(matched)
            msg = 'You will be reminded in ' + reminder_time + '. That\'s ' + str(total_seconds) + ' seconds! \n'
            msg += ''
            Timer(total_seconds, sendReminder, (self, messageObj, reminder)).start()
        else:
            msg = 'Usage: /remind <text> <1d|2h|43m|3s>'

        self.sendMessage(chat_id=messageObj.get('chat').get('id'),
                         text=msg.format(user_name=messageObj.get('from').get('first_name'))
                         )
