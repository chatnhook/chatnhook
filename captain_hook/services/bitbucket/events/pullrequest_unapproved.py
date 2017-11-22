# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import BitbucketEvent

"""
Triggered when a pull request is assigned, unassigned, labeled, unlabeled, opened,
edited, closed, reopened, or synchronized.
Also triggered when a pull request review is requested, or when a review request is removed.
"""


class PullrequestUnapprovedEvent(BitbucketEvent):
    def process(self, request, body):
        pr = body.get('pullrequest', {})
        pr_link = pr.get('links', {}).get('self', {}).get('href', '').replace(
            'https://api.bitbucket.org/2.0/', '')

        params = {
            'username': body.get('actor', {}).get('username', ''),
            'user_link': body.get('actor', {}).get('links', {}).get('self', {}).get('href'),
            'pull_request_number': str(pr.get('id')),
            'pull_request_link': self.build_redirect_link(
                'bitbucket',
                'pullrequest_created',
                pr_link),
            'pull_request_title': pr.get('title', '').encode('utf-8'),
            'body': str(pr.get('description', '')).encode('utf-8').strip(),
            'repository_name': body.get('repository', {}).get('full_name', ''),
            'repository_link': body.get('repository', {}).get('links', {}).get('html').get('href'),
            'state': 'unapproved',
            'icon': "🔴"
        }

        message = "[{icon}]({pull_request_link}) [{username}]({user_link}) {state} " \
                  "pull request " \
                  "[#{pull_request_number} {pull_request_title}]({pull_request_link})" \
                  " in [{repository_name}]({repository_link})"
        message = message.format(**params)

        return {"default": str(message)}

    def get_redirect(self, request, event, params):
        api_result = self.bb_api(params)
        status_code = 200
        if not api_result:
            return {
                'status_code': 404
            }

        s = api_result.get('links', {}).get('html', {}).get('href').split('/')
        repo = s[3] + '/' + s[4]

        title = '{issue_title} · PR #{issue_number} · {repo}'.format(
            issue_title=api_result.get('title').encode('utf-8'),
            issue_number=str(api_result.get('id')),
            repo=repo)

        redirect = {
            'meta_title': title,
            'meta_summary': '',
            'poster_image': api_result.get('author', {}).get('links', {}).get('avatar', {})
                .get('href'),

            'redirect': api_result.get('links', {}).get('html', {}).get('href'),
            'status_code': status_code,
        }
        return redirect
