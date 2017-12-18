# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base import BaseCommand


class ModlistCommand(BaseCommand):
    def get_description(self):
        return "Get information about you permissions"

    def run(self, messageObj, config):
        admins = self.config.get('permissions', {}).get('admins')
        moderators = self.config.get('permissions', {}).get('moderators')
        message = ''
        if admins:
            message += '⭐ *Administrators ({count})*\n'.format(count=len(admins))
            for admin in admins:
                message += '└ @{user}\n'.format(user=admin)

        if moderators:
            message += '👥 *Moderators ({count})*\n'.format(count=len(moderators))
            for moderator in moderators:
                message += '└ @{user}\n'.format(user=moderator)

        self.send_message(
            chat_id=messageObj.get('chat').get('id'),
            text=message)
