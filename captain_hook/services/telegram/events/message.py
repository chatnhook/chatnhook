# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from ...base.events import BaseEvent
import threading
import importlib
from utils import strings
import logging
import os

log = logging.getLogger('hookbot')


class MessageEvent(BaseEvent):
    def process(self, request, body):
        update = body
        self._call_services(update.get('message'))

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
            command_module = self._import_module('commands', 'core', command)
        except ImportError:
            try:
                command_module = self._import_module('commands', 'custom', command)
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

    def _import_module(self, type, which, command):
        package = "services.telegram.{}.{}.{}.{}".format(
            type,
            which,
            command,
            command
        )
        return importlib.import_module(package)

    def _call_services(self, message):
        dir_path = os.path.dirname(os.path.realpath(os.path.dirname(__file__))) + '/services/core'
        command_list = os.walk(dir_path).next()[1]
        for service in command_list:
            if service[0] is not '.':
                service_module = self.process_service(service)
                if service_module:
                    t = threading.Thread(target=service_module.run,
                                         args=(message, self.config))
                    t.start()

    def process_service(self, service):
        service_module = False
        try:
            service_module = self._import_module('services', 'core', service)
        except ImportError as e:

            try:
                service_module = self._import_module('commands', 'custom', service)
            except ImportError as e:
                print(str(e))
                log.warn("Don't know how to handle telegram command {}".format(service))

        service_processor_class_name = "{}Service".format(
            strings.toCamelCase(service),
        )
        if service_module:
            return getattr(service_module, service_processor_class_name)(
                config=self.config,
            )
