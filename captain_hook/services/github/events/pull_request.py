# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import GithubEvent

"""
Triggered when a pull request is assigned, unassigned, labeled, unlabeled, opened,
edited, closed, reopened, or synchronized.
Also triggered when a pull request review is requested, or when a review request is removed.
"""


class PullRequestEvent(GithubEvent):
    def process(self, request, body):

        pr_link = str(body.get('pull_request', {}).get('url')).replace(
            'https://api.github.com/', '')

        params = {
            'username': body.get('sender', {}).get('login', ''),
            'user_link': body.get('sender', {}).get('html_url', ''),
            'pull_request_number': str(body.get('pull_request', {}).get('number')),
            'pull_request_link': self.build_redirect_link('github', 'pull_request', pr_link),
            'pull_request_title': body.get('pull_request', {}).get('title', '').encode('utf-8'),
            'body': str(body.get('pull_request', {}).get('body', '')).encode('utf-8').strip(),
            'repository_name': body.get('repository', {}).get('full_name', ''),
            'repository_link': body.get('repository', {}).get('html_url', ''),
        }
        message = False

        if body['action'] == 'opened':
            message = "[⛓]({pull_request_link}) [{username}]({user_link}) opened new" \
                      " pull request " \
                      "[#{pull_request_number} {pull_request_title}]({pull_request_link})" \
                      " in [{repository_name}]({repository_link})"

        if body['action'] == 'reopened':
            message = "[⛓]({pull_request_link}) [{username}]({user_link}) reopened" \
                      " pull request " \
                      "[#{pull_request_number} {pull_request_title}]({pull_request_link})" \
                      " in [{repository_name}]({repository_link})"

        if body['action'] == 'edited':
            message = "[⛓]({pull_request_link}) [{username}]({user_link}) edited" \
                      " pull request " \
                      "[#{pull_request_number} {pull_request_title}]({pull_request_link})" \
                      " in [{repository_name}]({repository_link})"

        if body['action'] == 'updated':
            message = "[⛓]({pull_request_link}) [{username}]({user_link}) updated" \
                      " pull request " \
                      "[#{pull_request_number} {pull_request_title}]({pull_request_link})" \
                      " in [{repository_name}]({repository_link})"

        if body['action'] == 'closed' and body['pull_request']['merged'] is True:
            message = "[⛓]({pull_request_link}) [{username}]({user_link}) merged" \
                      " pull request " \
                      "[#{pull_request_number} {pull_request_title}]({pull_request_link})" \
                      " in [{repository_name}]({repository_link})"

        if body['action'] == 'closed' and body['pull_request']['merged'] is False:
            message = "[⛓]({pull_request_link}) [{username}]({user_link}) closed" \
                      " pull request " \
                      "[#{pull_request_number} {pull_request_title}]({pull_request_link})" \
                      " in [{repository_name}]({repository_link})"

        message = message.format(**params)

        return {"default": str(message)}

    def get_redirect(self, request, event, params):
        api_result = self.gh_api(params)
        status_code = 200
        if not api_result:
            return {
                'status_code': 404
            }

        if "message" in api_result and ("Not" in api_result.get('message') or
                                        "rate limit" in api_result.get('message')):
            return {
                'status_code': 404
            }
        s = api_result.get('url').split('/')
        repo = s[4] + '/' + s[5]
        if api_result['state'] == 'closed':
            status_code = 404
        title = '{issue_title} · PR #{issue_number} · {repo}'.format(
            issue_title=api_result.get('title').encode('utf-8'),
            issue_number=str(api_result.get('number')),
            repo=repo)

        redirect = {
            'meta_title': title,
            'meta_summary': api_result.get('body').split("\n")[0][0:100],
            'poster_image': api_result.get('user', {}).get('avatar_url'),
            'redirect': api_result.get('html_url', ''),
            'status_code': status_code,
        }
        return redirect
