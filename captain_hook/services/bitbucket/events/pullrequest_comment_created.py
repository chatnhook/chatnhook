# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import BitbucketEvent


class PullrequestCommentCreatedEvent(BitbucketEvent):
    """
    Triggered when an issue comment is created, edited, or deleted.
    """
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
                'pullrequest_comment_created',
                comment_api_link
            ),
            'issue_link': self.build_redirect_link(
                'bitbucket',
                'pullrequest_comment_created',
                issue_api_link
            ),
            'issue_title': pr.get('title').encode('utf-8'),
            'body': body_txt.split("\n")[0] + '...',
        }

        message = "[🗨]({comment_link}) [{username}]({user_link}) commented " \
                  "on PR [#{issue_number} {issue_title}]({comment_link})"
        message = message.format(**params)

        return {"default": str(message)}

    def get_redirect(self, request, event, params):
        api_result = self.bb_api(params)
        pr = api_result.get('pullrequest')
        status_code = 200
        if not api_result:
            status_code = 404

        issue_type = 'Pull Request'

        s = pr.get('links', {}).get('html', {}).get('href').split('/')

        repo = s[3] + '/' + s[4]
        title = '{username} replied · {issue_title} · {issue_type} #{issue_number} · {repo}'.format(
            issue_title=pr.get('title').encode('utf-8'), issue_number=str(pr.get('id')),
            repo=repo,
            username=api_result.get('user', {}).get('username', ''),
            issue_type=issue_type)
        redirect = {
            'meta_title': title,
            'meta_summary': api_result.get('content', {}).get('raw')
                                      .encode('utf-8').split("\n")[0][0:100],
            'poster_image': api_result.get('user', {}).get('links', {}).get('avatar', {})
                                      .get('href'),
            'redirect': api_result.get('links', {}).get('html', {}).get('href'),
            'status_code': status_code,
        }
        return redirect
