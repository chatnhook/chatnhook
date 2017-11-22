# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import BitbucketEvent

"""
Triggered when a commit comment is created.
"""


class RepoCommitCommentCreatedEvent(BitbucketEvent):
    def process(self, request, body):
        comment_api_link = str(body.get('comment', {}).get('links', {})
                               .get('self', {}).get('href'))\
            .replace('https://api.bitbucket.org/2.0/', '')

        redir_link = self.build_redirect_link(
            'bitbucket',
            'repo_commit_comment_created',
            comment_api_link)

        params = {
            'username': body.get('comment', {}).get('user', {}).get('username', ''),
            'user_link': body.get('comment', {}).get('user', {}).get('links', {}).get('html').get(
                'href'),
            'commit_hash': str(body.get('comment', {}).get('commit', {}).get('hash'))[:7],
            'commit_comment_link': redir_link,
            'body': str(body.get('comment', {}).get('content', {}).get('raw')).split("\n")[0],
        }

        message = "[🗨]({commit_comment_link}) [{username}]({user_link}) " \
                  "commented on [{commit_hash}]({commit_comment_link})"

        message = message.format(**params)

        return {"default": str(message)}

    def get_redirect(self, request, event, params):
        api_result = self.bb_api(params)
        status_code = 200
        if not api_result:
            status_code = 404

        s = api_result.get('commit', {}).get('links', {}).get('html', {}).get('href').split('/')

        repo = s[3] + '/' + s[4]
        title = '{username} commented on commit `{commit}` · {repo}'
        redirect = {
            'meta_title': title.format(username=api_result.get('user', {}).get('username', ''),
                                       commit=api_result.get('commit', {}).get('hash', '')[:7],
                                       repo=repo),
            'meta_summary': api_result.get('content', {}).get('raw', '').split("\n")[0][0:100],
            'poster_image': api_result.get('user', {}).get('links', {}).get('avatar', {}).get(
                'href'),
            'redirect': api_result.get('links', {}).get('html', {}).get('href'),
            'status_code': status_code,
        }
        return redirect
