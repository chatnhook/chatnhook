# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import BitbucketEvent


class IssueCreatedEvent(BitbucketEvent):
    """
    Triggered when a pull request is assigned, unassigned, labeled, unlabeled, opened,
    edited, closed, reopened, or synchronized.
    Also triggered when a pull request review is requested, or when a review request is removed.
    """
    def process(self, request, body):
        issue = body.get('issue', {})
        issue_link = issue.get('links', {}).get('self', {}).get('href', '').replace(
            'https://api.bitbucket.org/2.0/', '')

        params = {
            'username': body.get('actor', {}).get('username', ''),
            'user_link': body.get('actor', {}).get('links', {}).get('self', {}).get('href'),
            'issue_number': str(issue.get('id')),
            'issue_link': self.build_redirect_link(
                'bitbucket',
                'issue_created',
                issue_link),
            'issue_title': issue.get('title', '').encode('utf-8'),
            'body': str(issue.get('content', '')).encode('utf-8').strip(),
            'repository_name': body.get('repository', {}).get('full_name', ''),
            'repository_link': body.get('repository', {}).get('links', {}).get('html').get('href'),
        }
        message = "[⛓]({issue_link}) [{username}]({user_link}) opened new" \
                  " issue " \
                  "[#{issue_number} {issue_title}]({issue_link})" \
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

        if "message" in api_result and ("Not" in api_result.get('message') or
                                        "rate limit" in api_result.get('message')):
            return {
                'status_code': 404
            }
        s = api_result.get('links', {}).get('html', {}).get('href').split('/')
        repo = s[3] + '/' + s[4]

        if api_result.get('state') == 'MERGED' or api_result.get('state') == 'DECLINED':
            status_code = 404

        title = '{issue_title} · Issue #{issue_number} · {repo}'.format(
            issue_title=api_result.get('title').encode('utf-8'),
            issue_number=str(api_result.get('id')),
            repo=repo)

        redirect = {
            'meta_title': title,
            'meta_summary': api_result.get('content').get('raw').split("\n")[0][0:100],
            'poster_image': api_result.get('reporter', {}).get('links', {}).get('avatar', {})
                                      .get('href'),

            'redirect': api_result.get('links', {}).get('html', {}).get('href'),
            'status_code': status_code,
        }
        return redirect
