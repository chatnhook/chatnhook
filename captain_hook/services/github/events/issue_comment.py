# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import GithubEvent

"""
Triggered when an issue comment is created, edited, or deleted.
"""


class IssueCommentEvent(GithubEvent):
    def process(self, request, body):
        issue_type = 'issue'
        if 'pull_request' in body.get('issue', ''):
            issue_type = 'pull request'

        comment_api_link = str(body.get('comment', {}).get('url', '')).replace(
            'https://api.github.com/', '')
        issue_api_link = str(body.get('issue', {}).get('url', '')).replace(
            'https://api.github.com/', '')

        body_txt = body.get('comment', {}).get('body', '').encode('utf-8')

        params = {
            'username': body.get('sender', {}).get('login', ''),
            'user_link': body.get('sender', {}).get('html_url', ''),
            'sender': body.get('sender', {}).get('login', ''),
            'sender_link': body.get('sender', {}).get('html_url', ''),
            'issue_number': str(body.get('issue', {}).get('number', '')),
            'comment_link': self.build_redirect_link('github', 'issue_comment', comment_api_link),
            'issue_link': self.build_redirect_link('github', 'issues', issue_api_link),
            'issue_title': body.get('issue', {}).get('title').encode('utf-8'),
            'issue_type': issue_type,
            'body': body_txt.split("\n")[0] + '...',
        }
        message = ''
        if body.get('action') == 'created':
            message = "[🗨]({comment_link}) [{username}]({user_link}) commented " \
                      "on {issue_type} [#{issue_number} {issue_title}]({comment_link})"
        # message += '```{body}```'

        if body.get('action') == 'edited':
            message = "[🗨]({comment_link}) [{username}]({user_link}) edited the" \
                      " comment on {issue_type} [#{issue_number} {issue_title}]({comment_link})"

        if body.get('action') == 'deleted':
            message = "[❌]({issue_link}) [{sender}]({sender_link}) removed a" \
                      " comment on {issue_type} [#{issue_number} {issue_title}]({issue_link})"
        # message += '```{body}```'
        message = message.format(**params)

        return {"default": str(message)}

    def get_redirect(self, request, event, params):
        api_result = self.gh_api(params)

        status_code = 200
        if not api_result:
            status_code = 404

        issue_type = 'Issue'
        if 'pull_request' in api_result:
            issue_type = 'Pull Request'
        issue = self.gh_api(api_result.get('issue_url', ''))
        s = api_result.get('url', '').split('/')
        repo = s[4] + '/' + s[5]
        title = '{username} replied · {issue_title} · {issue_type} #{issue_number} · {repo}'.format(
            issue_title=issue.get('title').encode('utf-8'), issue_number=str(issue.get('number')),
            repo=repo,
            username=api_result.get('user', {}).get('login', ''),
            issue_type=issue_type)
        redirect = {
            'meta_title': title,
            'meta_summary': api_result.get('body', '').encode('utf-8').split("\n")[0][0:100],
            'poster_image': api_result.get('user', {}).get('avatar_url'),
            'redirect': api_result.get('html_url', ''),
            'status_code': status_code,
        }
        return redirect
