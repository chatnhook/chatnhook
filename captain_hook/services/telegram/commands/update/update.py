# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ..base import BaseCommand
import os
import git


class UpdateCommand(BaseCommand):
    def get_description(self):
        return "Get information about you permissions"

    def run(self, messageObj, config):
        username = messageObj.get('from', {}).get('username', '')

        if not self.is_admin(username):
            message = 'You don\'t have access to this command!'
            self.send_message(
                chat_id=messageObj.get('chat').get('id'),
                text=message)

        else:
            message = 'Updating and restarting!'
            self.send_message(
                chat_id=messageObj.get('chat').get('id'),
                text=message)
            git_repo = git.Repo(__file__, search_parent_directories=True)
            git_root = git_repo.git.rev_parse("--show-toplevel")
            try:
                origin = git_repo.remotes.origin
                origin.pull()
            except git.GitCommandError:
                pass

            os.system(git_root+'/restart.sh')
