# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base import BaseCommand


class RankCommand(BaseCommand):
    def get_description(self):
        return "Get information about you permissions"

    def run(self, messageObj, config):
        username = messageObj.get('from', {}).get('username', '')
        rank = self.get_rank(username)

        message = 'Hi {username}! You rank is *{rank}*'.format(username=username, rank=rank)
        self.send_message(
            chat_id=messageObj.get('chat').get('id'),
            text=message)
