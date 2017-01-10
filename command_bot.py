# -*- coding: utf-8 -*-
#
# Copyright (C) 2014, 2015, 2016 Sander Brand
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from os.path import abspath, normpath, dirname, join
from telegram.ext import Updater, CommandHandler
import telegram
from json import loads, dumps
from threading import Timer
import sys
import re
import logging
import datetime
import random

# logging.basicConfig(stream=stderr)
logging.basicConfig(level=logging.INFO)
from pprint import pprint

path = normpath(abspath(dirname(__file__)))
# Load config

with open(join(path, 'config.json'), 'r') as cfg:
    config = loads(cfg.read())

up = Updater(token=config['telegram_token'])
dispatcher = up.dispatcher


# Home function
def start(bot, update):
    # Home message
    msg = "Hello {user_name}! I'm {bot_name}. \n"
    msg += "What would you like to do? \n"
    msg += "/remind [text] [time]   \n"
    msg += "Time can be (for example) 2h or 60m "
    msg += "/info + username - shows your information \n"

    # Send the message
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg.format(
                         user_name=update.message.from_user.first_name,
                         bot_name=bot.name))


def sendReminder(bot, update, reminder):
    msg = 'Hey {user_name}, this is a reminder for:\n' + reminder
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg.format(
                         user_name=update.message.from_user.first_name,
                         bot_name=bot.name))


# Function to list the repositories
def remind(bot, update, args):
    message = ' '.join(args)

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
        Timer(total_seconds, sendReminder, (bot, update, reminder)).start()
    else:
        msg = 'Usage: /remind <text> <1d|2h|43m|3s>'

    bot.send_message(chat_id=update.message.chat_id,
                     text=msg.format(
                         user_name=update.message.from_user.first_name,
                         bot_name=bot.name))


def randomChoise(bot, update, args):
    message = ' '.join(args)
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

    bot.send_message(chat_id=update.message.chat_id,
                     text=msg.format(
                         user_name=update.message.from_user.first_name,
                         bot_name=bot.name))


def play8ball(bot, update, args):
    if len(args) == 0:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Usage: /8ball <question>')
        return

    choices = [
        'Without a doubt',
        'You may rely on it',
        'Do not count on it',
        'Looking good',
        'Cannot predict now',
        'It is decidedly so',
        'Outlook not so good'
    ]

    answer = random.choice(choices)
    bot.send_message(chat_id=update.message.chat_id,
                     text=answer)


# Add handlers to dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('remind', remind, pass_args=True))
dispatcher.add_handler(CommandHandler('random', randomChoise, pass_args=True))
dispatcher.add_handler(CommandHandler('8ball', play8ball, pass_args=True))

# Start the program
try:
    up.start_polling()
except KeyboardInterrupt:
    # quit
    sys.exit()
