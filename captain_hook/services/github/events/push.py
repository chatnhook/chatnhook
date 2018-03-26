# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import GithubEvent

"""
Triggered on a push to a repository branch.
Branch pushes and repository tag pushes also trigger webhook push events.

Note: The webhook payload example following the table differs significantly
from the Events API payload described in the Github API. Among other differences,
the webhook payload includes both sender and pusher objects.
Sender and pusher are the same user who initiated the push event,
but the sender object contains more detail.
"""


class PushEvent(GithubEvent):
    def process(self, request, body):
        plural = 'changesets'
        branch = body.get('ref', '').split('/')[2]
        branches = self.project_service_config.get('settings', {}).get('notify_branches', [])
        if branches and branch not in branches:
            return False

        if len(body.get('commits')) == 1:
            plural = 'changeset'

        push_link = body.get('compare').replace('https://github.com/', '')
        user_link = body.get('sender', {}).get('html_url').replace(
            'https://github.com/', '')
        repo_link = body.get('repository', {}).get('html_url')\
            .replace('https://github.com/', '')

        branch_link = body.get('repository', {}).get('branches_url')\
            .replace('{/branch}', '/'+branch).replace('https://api.github.com/repos/', '')

        params = {
            'username': body.get('sender', {}).get('login', ''),
            'user_link': self.build_redirect_link('github', 'push', user_link),
            'commit_amount': len(body.get('commits', '')),
            'plural': plural,
            'repository_name': body.get('repository', {}).get('full_name', ''),
            'repository_link': self.build_redirect_link('github', 'push', repo_link),
            'branch_link': self.build_redirect_link('github', 'push', branch_link),
            'push_link': self.build_redirect_link('github', 'push', push_link),
            'ref': body.get('ref', '').replace('refs/heads/', ''),
        }

        message = "[🔨]({push_link}) [{username}]({user_link}) pushed {commit_amount} " \
                  "{plural} to [{ref}]({branch_link}) at [{repository_name}]({repository_link}): \n"

        # message += '```{body}```'
        message = message.format(**params)

        for commit in body.get('commits'):
            args = {
                'commit_hash': str(commit.get('id'))[:7],
                'commit_message': commit.get('message', '').encode('utf-8').replace("\n\n", '\n'),
                'commit_link': commit.get('url', '')
            }
            message += "· [{commit_hash}]({commit_link}): {commit_message} \n".format(
                **args)

        return {"default": str(message)}

    def get_redirect(self, request, event, params):
        redirect = {
            'meta_title': '',
            'meta_summary': '',
            'poster_image': '',
            'redirect': 'https://github.com/' + params,
            'status_code': 404
        }
        return redirect
