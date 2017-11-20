# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import BitbucketEvent

"""
Triggered when a user forks a repository.
"""


class RepoForkEvent(BitbucketEvent):
    def process(self, request, body):
        user_link = body.get('actor', {}).get('links', {}) \
            .get('html').get('href').replace('https://bitbucket.org/', '')
        repo_link = body.get('repository', {}).get('links', {}) \
            .get('html').get('href').replace('https://bitbucket.org/', '')

        fork_link = body.get('fork', {}).get('links', {}) \
            .get('html').get('href').replace('https://bitbucket.org/', '')

        params = {
            'username': body.get('actor', {}).get('username', ''),
            'user_link': self.build_redirect_link('bitbucket', 'repo_fork', user_link),
            'repository_name': body.get('repository', {}).get('full_name', ''),
            'repository_link': self.build_redirect_link('bitbucket', 'repo_fork', repo_link),
            'fork_name': body.get('fork', {}).get('full_name', ''),
            'fork_url': self.build_redirect_link('bitbucket', 'repo_fork', fork_link),
        }

        message = "🔀 [{username}]({user_link}) forked [{repository_name}]({repository_link}) " \
                  "to [{fork_name}]({fork_url})"
        message = message.format(**params)
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
