# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base import BaseCommand


class SpamCommand(BaseCommand):
    def get_description(self):
        return "Mark a message as spam"

    def run(self, messageObj, config):
        user = messageObj.get('from', {}).get('username')
        if not self.is_admin(user) and not self.is_moderator(user):
            return

        forwarded_message = messageObj.get('reply_to_message', {})
        print forwarded_message
