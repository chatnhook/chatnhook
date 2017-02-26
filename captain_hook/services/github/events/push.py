# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class PushEvent(BaseEvent):

    def process(self):
        plural = 'changesets'
        branch =  self.body['ref'].split('/')[2]


        if branch not in self.config['notify_branches']:
            return False

        if len(self.body['commits']) == 1:
            plural = 'changeset'
        params = {
            'username': self.body['sender']['login'],
            'user_link': self.body['sender']['html_url'],
            'commit_amount': len(self.body['commits']),
            'plural': plural,
            'repository_name': self.body['repository']['full_name'],
            'repository_link': self.body['repository']['html_url'],
            'push_link': self.body['compare'],
            'ref': ref[2],
        }

        message = "[🔨]({push_link}) [{username}]({user_link}) pushed {commit_amount} {plural} to {ref} at [{repository_name}]({repository_link}): \n"

        # message += '```{body}```'
        message = message.format(**params)

        for commit in self.body['commits']:
            args = {
                'commit_hash': str(commit['id'])[:7],
                'commit_message': commit['message'].replace("\n\n", '\n'),
                'commit_link':  commit['html_url']
            }
            message += "· [{commit_hash}]({commit_link}): {commit_message} \n".format(**args)

        return {"telegram": str(message)}