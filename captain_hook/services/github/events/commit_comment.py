# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import GithubEvent

"""
Triggered when a commit comment is created.
"""


class CommitCommentEvent(GithubEvent):
    def process(self, request, body):

        comment_api_link = str(body.get('comment', {}).get('url')).replace(
            'https://api.github.com/', '')
        redir_link = self.build_redirect_link('github', 'commit_comment', comment_api_link)
        params = {
            'username': body.get('sender', {}).get('login', ''),
            'user_link': body.get('sender', {}).get('html_url', ''),
            'commit_hash': str(body.get('comment', {}).get('commit_id', ''))[:7],
            'commit_comment_link': redir_link,
            'body': str(body.get('comment', {}).get('body', '')).split("\n")[0],
        }

        message = False
        if body.get('action') == 'created':
            message = "[🗨]({commit_comment_link}) [{username}]({user_link}) " \
                      "commented on [{commit_hash}]({commit_comment_link})"
            # message += '```{body}```'
            message = message.format(**params)

        if body.get('action') == 'edited':
            message = "[🗨]({commit_comment_link}) [{username}]({user_link}) edited " \
                      "the comment on [{commit_hash}]({commit_comment_link})"
            # message += '```{body}```'
            message = message.format(**params)

        return {"default": str(message)}

    def get_redirect(self, request, event, params):
        api_result = self.gh_api(params)
        status_code = 200
        if not api_result:
            status_code = 404

        if "Not" in api_result.get('message'):
            return {
                'status_code': 404
            }

        s = api_result.get('url', '').split('/')
        repo = s[4] + '/' + s[5]
        title = '{username} commented on commit `{commit}` · {repo}'
        redirect = {
            'meta_title': title.format(username=api_result.get('user', {}).get('login', ''),
                                       commit=api_result.get('commit_id', '')[:7],
                                       repo=repo),
            'meta_summary': api_result.get('body').split("\n")[0][0:100],
            'poster_image': api_result.get('user', {}).get('avatar_url'),
            'redirect': api_result.get('html_url', ''),
            'status_code': status_code,
        }
        return redirect
