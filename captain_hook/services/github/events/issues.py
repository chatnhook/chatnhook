# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import GithubEvent

"""
Triggered when an issue is assigned, unassigned, labeled,
unlabeled, opened, edited, milestoned, demilestoned, closed, or reopened.
"""


class IssuesEvent(GithubEvent):
    def process(self, request, body):

        issue_link = str(body.get('issue', {}).get('url', '')).replace(
            'https://api.github.com/', '')

        params = {
            'username': body.get('sender', {}).get('login', ''),
            'user_link': body.get('sender', {}).get('html_url', ''),
            'issue_number': str(body.get('issue', {}).get('number', '')),
            'issue_link': self.build_redirect_link('github', 'issues', issue_link),
            'issue_title': body.get('issue', {}).get('title').encode('utf-8'),
            'body': body.get('issue', {}).get('body'),
            'repository_name': body.get('repository', {}).get('full_name', ''),
            'repository_link': body.get('repository', {}).get('html_url', ''),
        }
        message = False
        if body['action'] == 'opened':
            message = "[❓]({issue_link}) [{username}]({user_link}) " \
                      "opened new issue [#{issue_number}{issue_title}]({issue_link}) " \
                      "in [{repository_name}]({repository_link})"

        if body['action'] == 'reopened':
            message = "[❓]({issue_link}) [{username}]({user_link}) " \
                      "reopened issue [#{issue_number} {issue_title}]({issue_link}) " \
                      "in [{repository_name}]({repository_link})"

        if body['action'] == 'edited':
            message = "[❓]({issue_link}) [{username}]({user_link}) edited issue [#{issue_number} " \
                      "{issue_title}]({issue_link}) in [{repository_name}]({repository_link})"

        if body['action'] == 'closed':
            message = "[❓]({issue_link}) [{username}]({user_link}) closed issue [#{issue_number} " \
                      "{issue_title}]({issue_link}) in [{repository_name}]({repository_link})"

        message = message.format(**params)

        return {"default": str(message)}

    def get_redirect(self, request, event, params):
        api_result = self.gh_api(params)
        status_code = 200
        if not api_result:
            status_code = 404
        s = api_result.get('url').split('/')
        repo = s[4] + '/' + s[5]

        if api_result['state'] == 'closed':
            status_code = 404

        redirect = {
            'meta_title': '{issue_title} · Issue #{issue_number} · {repo}'.format(
                issue_title=api_result.get('title').encode('utf-8'),
                issue_number=str(api_result.get('number')),
                repo=repo),
            'meta_summary': api_result.get('body').split("\n")[0][0:100],
            'poster_image': api_result.get('user', {}).get('avatar_url'),
            'redirect': api_result.get('html_url', ''),
            'status_code': status_code,
        }
        return redirect
