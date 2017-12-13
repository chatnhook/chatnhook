# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ..base import BaseCommand
import os
import importlib
from utils import strings


class StartCommand(BaseCommand):
    def get_description(self):
        return "You just ran it!"

    def run(self, messageObj, config):
        msg = 'Welcome to this bot!\n'
        dir_path = os.path.dirname(os.path.realpath(os.path.dirname(__file__)))
        command_list = os.walk(dir_path).next()[1]
        del command_list[command_list.index('base')]
        del command_list[command_list.index('custom')]

        dir_path = os.path.dirname(os.path.realpath(os.path.dirname(__file__))) + '/custom'
        custom_command_list = os.walk(dir_path).next()[1]
        command_list = command_list + custom_command_list

        commands = []

        for command in command_list:
            try:
                command_class = self.process_command(command)
                help_string = command_class.get_description()
            except AttributeError:
                help_string = 'No help available'

            commands.append('/{} - {}'.format(command, help_string))
        msg += 'Available commands:\n ' + '\n'.join(commands)
        self.send_message(parse_mode='HTML', chat_id=messageObj.get('chat').get('id'), text=msg)

    def process_command(self, command):
        command_module = False
        try:
            command_module = self._import_command_module(command)
        except ImportError:
            command_module = self._import_custom_command_module(command)

        command_processor_class_name = "{}Command".format(
            strings.toCamelCase(command),
        )
        if command_module:
            return getattr(command_module, command_processor_class_name)(
                config=self.config,
            )
        return False

    def _import_command_module(self, command):
        package = "services.telegram.commands.{}.{}".format(
            command,
            command
        )
        return importlib.import_module(package)

    def _import_custom_command_module(self, command):
        package = "services.telegram.commands.custom.{}.{}".format(
            command,
            command
        )
        return importlib.import_module(package)
