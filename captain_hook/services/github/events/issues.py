# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class IssuesEvent(BaseEvent):
    def process(self, request, body):

        issue_link = str(body['issue']['url']).replace('https://api.github.com/', '')

        params = {
            'username': body['sender']['login'],
            'user_link': body['sender']['html_url'],
            'issue_number': str(body['issue']['number']),
            'issue_link': self.build_redirect_link('github', 'issues', issue_link),
            'issue_title': body['issue']['title'],
            'body': body['issue']['body'],
            'repository_name': body['repository']['full_name'],
            'repository_link': body['repository']['html_url'],
        }
        message = False
        if body['action'] == 'opened':
            message = "[❓]({issue_link}) [{username}]({user_link}) opened new issue [#{issue_number} " \
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
        s = api_result['url'].split('/')
        repo = s[4] + '/' + s[5]

        if api_result['state'] == 'closed':
            status_code = 404

        redirect = {
            'meta_title': '{issue_title} · Issue #{issue_number} · {repo}'.format(
                issue_title=api_result['title'], issue_number=str(api_result['number']), repo=repo),
            'meta_summary': api_result['body'].split("\n")[0][0:100],
            'poster_image': api_result['user']['avatar_url'],
            'redirect': api_result['html_url'],
            'status_code': status_code,
        }
        return redirect
