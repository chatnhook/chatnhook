from __future__ import absolute_import
from ..base import BaseService
import telegram
from telegram.error import RetryAfter, TimedOut
from flask import g
from time import sleep
import os
import logging
from .events.message import MessageEvent
log = logging.getLogger('hookbot')


class TelegramService(BaseService):
    def register_webhook(self):
        self.telegram_webhook = telegram.Bot(self.config['token'])
        try:
            log.info('Unregistered telegram webhook url')
            self.telegram_webhook.setWebhook(url='')
            sleep(1)
            log.info('Cleaning updates')
            updates = []
            self.telegram_webhook.get_updates()
            sleep(1)
            log.info('Registering telegram webhook url: %s' % self.webhook_url)
            self.telegram_webhook.setWebhook(
                url=self.webhook_url,
                certificate=self.cert,
                allowed_updates=updates,
                max_connections=40)
            self.webhook = self.telegram_webhook.getWebhookInfo()
        except TimedOut as e:
            log.warn('Unable to reach telegram servers, retrying')
            self.register_webhook()
        except RetryAfter as e:
            log.warn('Throtteled! Sleeping for %s', e.retry_after)
            sleep(e.retry_after)
            self.register_webhook()

    def register_commands(self, return_commands=False):
        dir_path = os.path.dirname(os.path.realpath(__file__)) + '/commands/core'
        command_list = os.walk(dir_path).next()[1]
        dir_path = os.path.dirname(os.path.realpath(__file__)) + '/commands/custom'
        custom_commands = os.walk(dir_path).next()[1]

        custom_command_list = []
        for command in custom_commands:
            if command[0] is not '.':
                custom_command_list.append(command)

        # self.telegram_webhook.
        log.info('Found commands: ' + ', '.join(command_list))
        log.info('Found custom commands: ' + ', '.join(custom_command_list))

        if return_commands:
            return {'core': command_list, 'custom': custom_command_list }

    def get_command_modules(self):
        commands = self.register_commands(True)
        me = MessageEvent(self.config, self.config, None)
        command_modules = {}
        for type in commands:
            for command in commands[type]:
                command_module = me.process_command(command)
                command_modules[command] = command_module

        return command_modules

    def setup(self):
        if not self.config.get('enable_bot', False):
            log.info('Telegram bot is disabled. '
                     'Set services.telegram.enable_bot to true to enable it')
            return
        else:
            log.info('Init telegram bot...')

        self.cert = False
        if self.config['server_cert']:
            self.cert = open(self.config['server_cert'], 'rb')
        self.webhook = False
        self.webhook_url = 'https://%s:%s/telegram' % (
            self.config['hostname'], self.config['port'])

        try:
            self.register_webhook()
            self.register_commands()
        except telegram.error.RetryAfter as e:
            # @todo continues checking
            log.error('Error during signup at telegram')
            print(e)
            pass

        if self.webhook and self.webhook.last_error_date:
            # print ("last_error_date : %s" %
            # 	   datetime.datetime.fromtimestamp(
            # 		   int(self.webhook.last_error_date)
            # 	   ).strftime('%Y-%m-%d %H:%M:%S')
            # 	   )
            log.info("last_error_message : %s" % str(self.webhook.last_error_message))
            # print (self.telegram_webhook.getWebhookInfo())

    def get_event(self, request, body):
        return next(iter(body))

    def get_service_config_model(self):
        return [
            {
                'name': 'hostname',
                'label': 'Hostname',
                'type': 'text',
                'description': 'Hostname to register at telegram API'
            },
            {
                'name': 'server_cert',
                'label': 'Server certificate',
                'type': 'text',
                'description': ''
            },
            {
                'name': 'token',
                'label': 'Bot token',
                'type': 'text',
                'description': 'Your bot token'
            },
        ]
