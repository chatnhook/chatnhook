# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import BitbucketEvent

"""
Triggered on a push to a repository branch.
Branch pushes and repository tag pushes also trigger webhook push events.

Note: The webhook payload example following the table differs significantly
from the Events API payload described in the Github API. Among other differences,
the webhook payload includes both sender and pusher objects.
Sender and pusher are the same user who initiated the push event,
but the sender object contains more detail.
"""


class RepoPushEvent(BitbucketEvent):
    def process(self, request, body):

        plural = 'changesets'

        branch = body.get('push', {}).get('changes', {})[0].get('new', {}).get('name', '')

        if self.config.get('notify_branches', False)\
                and branch not in self.config.get('notify_branches'):
            return False

        if len(body.get('push', {}).get('changes', {})) == 1:
            plural = 'changeset'
        #
        push_link = body.get('push', {}).get('changes', {})[0].get('new', {}).get('target', {}) \
            .get('links', {}).get('html', {}).get('href').replace('https://bitbucket.org/', '')

        user_link = body.get('actor', {}).get('links').get('html')\
            .get('href').replace('https://bitbucket.org/', '')
        repo_link = body.get('repository', {}).get('links', {}).get('html').get('href')\
            .replace('https://bitbucket.org/', '')

        params = {
            'username': body.get('actor', {}).get('username', ''),
            'user_link': self.build_redirect_link('bitbucket', 'repo_push', user_link),
            'commit_amount': len(body.get('push', {}).get('changes', {})),
            'plural': plural,
            'repository_name': body.get('repository', {}).get('full_name', ''),
            'repository_link': self.build_redirect_link('bitbucket', 'repo_push', repo_link),
            'push_link': self.build_redirect_link('github', 'push', push_link),
            'ref': branch,
        }

        message = "[🔨]({push_link}) [{username}]({user_link}) pushed {commit_amount} " \
                  "{plural} to {ref} at [{repository_name}]({repository_link}): \n"

        message = message.format(**params)
        #
        for change in body.get('push').get('changes'):
            for commit in change.get('commits'):
                args = {
                    'commit_hash': str(commit.get('hash'))[:7],
                    'commit_message': commit.get('message', '').encode('utf-8')
                                            .replace("\n\n", '\n'),
                    'commit_link': commit.get('links', {}).get('html', {}).get('href')
                }
                message += "· [{commit_hash}]({commit_link}): {commit_message} \n".format(
                    **args)

        return {"default": str(message)}

    def get_redirect(self, request, event, params):
        redirect = {
            'meta_title': '',
            'meta_summary': '',
            'poster_image': '',
            'redirect': 'https://bitbucket.org/' + params,
            'status_code': 404
        }
        return redirect
