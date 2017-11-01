# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent
import threading
import importlib
from utils import strings

class MessageEvent(BaseEvent):
    def process(self, request, body):
        update = body
        commandResponse = ''
        if update.get('message', '') and update.get('message').get('text') == 'ping':
            return {"telegram": str('Pong!')}
        else:
            message = update.get('message', '').get('text')
            if message and message[0][0] == '/':
                messageSplit = message[1:].split(' ')
                command = messageSplit[0]
                command_module = self.process_command(command)
                t = threading.Thread(target=command_module.run, args=(update.get('message'), self.config))
                t.start()

            return {"telegram": str('')}

    def process_command(self, command):
        self._import_command_module(command)
        try:
            command_module = self._import_command_module(command)
        except ImportError:
            print("Doesn't know how to handle telegram command {}".format(command))

        command_processor_class_name = "{}Command".format(
            strings.toCamelCase(command),
        )
        return getattr(command_module, command_processor_class_name)(
            config=self.config,
        )

    def _import_command_module(self, command):
        package = "services.telegram.commands.{}.{}".format(
            command,
            command
        )
        return importlib.import_module(package)
