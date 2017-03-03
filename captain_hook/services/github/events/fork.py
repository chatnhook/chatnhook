# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import GithubEvent


class ForkEvent(GithubEvent):

    def process(self, request, body):
        user_link = body['sender']['html_url'].replace('https://github.com/', '')
        repo_link = body['repository']['html_url'].replace('https://github.com/', '')
        fork_link = body['forkee']['html_url'].replace('https://github.com/', '')

        params = {
            'username': body['sender']['login'],
            'user_link': self.build_redirect_link('github', 'fork', user_link),
            'repository_name': body['repository']['full_name'],
            'repository_link': self.build_redirect_link('github', 'fork', repo_link),
            'fork_name': body.get('forkee').get('full_name'),
            'fork_url': self.build_redirect_link('github', 'fork', fork_link),
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
            'redirect': 'https://github.com/' + params,
            'status_code': 404
        }
        return redirect
