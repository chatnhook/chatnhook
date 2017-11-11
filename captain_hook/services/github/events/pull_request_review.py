# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import GithubEvent

"""
Triggered when a pull request review is submitted into a
non-pending state, the body is edited, or the review is dismissed.
"""


class PullRequestReviewEvent(GithubEvent):
    def process(self, request, body):
        user_link = body.get('sender', {}).get('html_url', '').replace(
            'https://github.com/', '')
        pr_link = body.get('pull_request', {}).get('html_url', '').replace(
            'https://github.com/', '')

        params = {'username': body.get('sender', {}).get('login'),
                  'user_link': self.build_redirect_link('github', 'release', user_link),
                  'pull_request_number': str(body.get('pull_request', {}).get('number')),
                  'pull_request_link': self.build_redirect_link('github', 'pull_request', pr_link),
                  'pull_request_title': body.get('pull_request', {}).get('title', ''),
                  'repository_name': body.get('repository', {}).get('full_name', ''),
                  'repository_link': body.get('repository', {}).get('html_url', ''),
                  'state': 'approved',
                  'icon': "✅"
                  }

        if body.get('review').get('state') == "changes_requested":
            params['state'] = 'requested changes on'
            params['icon'] = "🔴"

        message = "[{icon}]({pull_request_link}) [{username}]({user_link}) {state} " \
                  "pull request " \
                  "[#{pull_request_number} {pull_request_title}]({pull_request_link})" \
                  " in [{repository_name}]({repository_link})"
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
