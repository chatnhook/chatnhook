# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class PushEvent(BaseEvent):

    def process(self, request, body):
        plural = 'changesets'
        branch =  body['ref'].split('/')[2]


        if branch not in config['notify_branches']:
            return False

        if len(body['commits']) == 1:
            plural = 'changeset'
        params = {
            'username': body['sender']['login'],
            'user_link': body['sender']['html_url'],
            'commit_amount': len(body['commits']),
            'plural': plural,
            'repository_name': body['repository']['full_name'],
            'repository_link': body['repository']['html_url'],
            'push_link': body['compare'],
            'ref': ref[2],
        }

        message = "[🔨]({push_link}) [{username}]({user_link}) pushed {commit_amount} {plural} to {ref} at [{repository_name}]({repository_link}): \n"

        # message += '```{body}```'
        message = message.format(**params)

        for commit in body['commits']:
            args = {
                'commit_hash': str(commit['id'])[:7],
                'commit_message': commit['message'].replace("\n\n", '\n'),
                'commit_link':  commit['html_url']
            }
            message += "· [{commit_hash}]({commit_link}): {commit_message} \n".format(**args)

        return {"default": str(message)}
