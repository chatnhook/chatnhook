# -*- coding: utf-8 -*-
from __future__ import absolute_import
from captain_hook.services.telegram.commands.base import BaseCommand
from time import sleep
from pprint import pprint
import telegram


class SlapCommand(BaseCommand):
	def get_description(self):
		return "I smell fish..."

	def run(self, messageObj, config):
		self.sendMessage(chat_id=messageObj.get('chat').get('id'),
						 text='*Slaps {name} with a large trout'.format(name=', '.join(messageObj.get('args'))),
						 parse_mode=telegram.ParseMode.HTML
						 )
