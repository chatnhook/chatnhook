# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import BitbucketEvent

"""
Triggered when an issue comment is created, edited, or deleted.
"""


class PullrequestCommentDeletedEvent(BitbucketEvent):
    def process(self, request, body):
        comment = body.get('comment', {})
        pr = body.get('pullrequest', {})
        comment_api_link = str(comment.get('links', {}).get('self', {}).get('href')).replace(
            'https://api.bitbucket.org/2.0/', '')
        issue_api_link = str(pr.get('links', {}).get('self', {}).get('href')).replace(
            'https://api.bitbucket.org/2.0/', '')

        body_txt = comment.get('content', {}).get('raw', '').encode('utf-8')

        params = {
            'username': body.get('actor', {}).get('username', ''),
            'user_link': body.get('actor', {}).get('links', {}).get('html', {}).get('href'),
            'issue_number': str(pr.get('id', '')),
            'comment_link': self.build_redirect_link(
                'bitbucket',
                'pullrequest_comment_deleted',
                comment_api_link
            ),
            'issue_link': self.build_redirect_link(
                'bitbucket',
                'pullrequest_comment_deleted',
                issue_api_link
            ),
            'issue_title': pr.get('title').encode('utf-8'),
            'comment_user': comment.get('user', {}).get('username'),
            'body': body_txt.split("\n")[0] + '...',
        }

        message = "[🗨]({comment_link}) [{username}]({user_link}) " \
                  "removed a comment from {comment_user}" \
                      " on PR [#{issue_number} {issue_title}]({comment_link})"
        message = message.format(**params)

        return {"default": str(message)}

    def get_redirect(self, request, event, params):

        params = params.split('/')
        params = '/'.join(params[:len(params)-2])
        status_code = 404

        redirect = {
            'meta_title': '',
            'meta_summary': '',
            'poster_image': '',
            'redirect': 'https://bitbucket.com'+ params,
            'status_code': status_code,
        }
        return redirect
