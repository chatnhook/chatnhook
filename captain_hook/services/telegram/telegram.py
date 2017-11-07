from __future__ import absolute_import
from ..base import BaseService
import importlib
import telegram

from time import sleep
from pprint import pprint
import os
import datetime
from .events.message import MessageEvent


class TelegramService(BaseService):
    def registerWebhook(self):
        self.telegram_webhook = telegram.Bot(self.config['token'])
        print('Unregistered telegram webhook url')
        self.telegram_webhook.setWebhook(url='')
        sleep(1)
        print('Cleaning updates')
        updates = []
        self.telegram_webhook.get_updates()
        sleep(1)
        print('Registering telegram webhook url: %s' % self.webhook_url)
        self.telegram_webhook.setWebhook(
            url=self.webhook_url, certificate=self.cert, allowed_updates=updates, max_connections=40)
        self.webhook = self.telegram_webhook.getWebhookInfo()

    def registerCommands(self):
        dir_path = os.path.dirname(os.path.realpath(__file__)) + '/commands'
        command_list = os.walk(dir_path).next()[1]
        del command_list[command_list.index('base')]

        # self.telegram_webhook.
        print('Found commands:' + ', '.join(command_list))

    def setup(self):
        print('init telegram service')

        self.cert = False
        if self.config['server_cert']:
            self.cert = open(self.config['server_cert'], 'rb')
        self.webhook = False
        self.webhook_url = 'https://%s:%s/telegram' % (
            self.config['hostname'], self.config['port'])

        try:
            self.registerWebhook()
            self.registerCommands()
        except telegram.error.RetryAfter as e:
            # @todo continues checking
            print('Error during signup at telegram')
            print(e)
            pass

        if self.webhook and self.webhook.last_error_date:
            print ("last_error_date : %s" %
                   datetime.datetime.fromtimestamp(
                       int(self.webhook.last_error_date)
                   ).strftime('%Y-%m-%d %H:%M:%S')
                   )
            print ("last_error_message : %s" % str(self.webhook.last_error_message))
            # print (self.telegram_webhook.getWebhookInfo())

    def get_event(self, request, body):
        if 'message' in body:
            return 'message'
