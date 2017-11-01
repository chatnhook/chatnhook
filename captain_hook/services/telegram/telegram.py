from __future__ import absolute_import
from ..base import BaseService
import telegram
from time import sleep
import datetime


class TelegramService(BaseService):
    def setup(self):
        print('init telegram service')

        cert = False
        if self.config['server_cert']:
            cert = open(self.config['server_cert'], 'rb')

        webhook_url = 'https://%s:%s/telegram' % (
            self.config['hostname'], self.config['port'])
        print('Registering telegram webhook url: %s' % webhook_url)
        self.telegram_webhook = telegram.Bot(self.config['token'])
        self.telegram_webhook.setWebhook(webhook_url='')
        sleep(0.1)
        updates = []
        self.telegram_webhook.setWebhook(
            webhook_url=webhook_url, certificate=cert, allowed_updates=updates)
        webhook = self.telegram_webhook.getWebhookInfo()
        print ("Webhook settings: \n")
        print ("URL : %s" % webhook.url)
        print ("has_custom_certificate : %s" %
               str(webhook.has_custom_certificate))

        if webhook.last_error_date:
            print ("last_error_date : %s" %
                   datetime.datetime.fromtimestamp(
                       int(webhook.last_error_date)
                   ).strftime('%Y-%m-%d %H:%M:%S')
                   )
            print ("last_error_message : %s" % str(webhook.last_error_message))
            # print (self.telegram_webhook.getWebhookInfo())

    def get_event(self, request, body):
        if 'edited_message' in body:
            return 'edited_message'
        else:
            return 'message'
