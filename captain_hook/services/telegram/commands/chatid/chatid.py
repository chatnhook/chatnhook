# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ..base import BaseCommand


class ChatidCommand(BaseCommand):
    @classmethod
    def get_description(self):
        return "Get the current chat id. Works for private and public channels."

    def run(self, messageObj, config):
        username = messageObj.get('from', {}).get('username', '')

        if not self.is_admin(username):
            message = 'You don\'t have access to this command!'
            self.send_message(
                chat_id=messageObj.get('chat').get('id'),
                text=message)
        else:
            message = "The channel id is: {channel}" \
                .format(channel=messageObj.get('chat').get('id'))

        self.send_message(
            chat_id=messageObj.get('chat').get('id'),
            text=message)
