# -*- coding: utf-8 -*-
from __future__ import absolute_import
from captain_hook.services.telegram.commands.base import BaseCommand
import os


class StartCommand(BaseCommand):
	def run(self, messageObj, config):
		msg = 'Welcome to this bot!'
		self.sendMessage(chat_id=messageObj.get('chat').get('id'), text=msg.format())
		dir_path = os.path.dirname(os.path.realpath(os.path.dirname(__file__)))
		command_list = os.walk(dir_path).next()[1]
		del command_list[command_list.index('base')]
		commands = []
		for command in command_list:
			commands.append('/{}'.format(command))
		self.sendMessage(chat_id=messageObj.get('chat').get('id'), text='Available commands: ' + ', '.join(commands))
