# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import GithubEvent


class CommitCommentEvent(GithubEvent):

    def process(self, request, body):

        comment_api_link = str(body['comment']['url']).replace(
            'https://api.github.com/', '')
        params = {
            'username': body['comment']['user']['login'],
            'user_link': body['comment']['user']['html_url'],
            'commit_hash': str(body['comment']['commit_id'])[:7],
            'commit_comment_link': self.build_redirect_link('github', 'commit_comment', comment_api_link),
            'body': str(body['comment']['body']).split("\n")[0],
        }

        message = False
        if body['action'] == 'created':
            message = "[🗨]({commit_comment_link}) [{username}]({user_link}) commented on [{commit_hash}]({commit_comment_link})"
            # message += '```{body}```'
            message = message.format(**params)

        if body['action'] == 'edited':
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

        redirect = {
            'meta_title': '',
            'meta_summary': '',
            'meta_link': '',
            'poster_image': '',
            'redirect': 'https://github.com/' + params,
            'status_code': status_code,
        }
        return redirect
