# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent
import threading
import importlib
from utils import strings
import logging

log = logging.getLogger('hookbot')


class MessageEvent(BaseEvent):
    def process(self, request, body):
        update = body
        if update.get('message', '') and update.get('message').get('text') == 'ping':
            return {"telegram": str('Pong!')}
        else:
            message = update.get('message', '').get('text')
            if message and message[0][0] == '/':
                messageSplit = message[1:].split(' ')
                if '@' in messageSplit[0]:
                    messageSplit = messageSplit[0].split('@')
                command = messageSplit[0]
                messageSplit.pop(0)
                update['message']['command'] = command
                update['message']['args'] = messageSplit
                if command == 'base':
                    return {'telegram': ''}
                try:
                    command_module = self.process_command(command)
                    if command_module:
                        t = threading.Thread(target=command_module.run,
                                             args=(update.get('message'), self.config))
                        t.start()
                except ImportError:
                    log.warn("Don't know how to handle telegram command {}".format(command))
                    return {"telegram": str('')}
            return {"telegram": str('')}

    def process_command(self, command):
        command_module = False
        try:
            command_module = self._import_command_module(command)
        except ImportError:
            try:
                command_module = self._import_custom_command_module(command)
            except ImportError as e:
                print(str(e))
                log.warn("Don't know how to handle telegram command {}".format(command))

        command_processor_class_name = "{}Command".format(
            strings.toCamelCase(command),
        )
        if command_module:
            return getattr(command_module, command_processor_class_name)(
                config=self.config,
            )
        return False

    def _import_command_module(self, command):
        package = "services.telegram.commands.core.{}.{}".format(
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
