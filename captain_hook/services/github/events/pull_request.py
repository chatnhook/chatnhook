# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import GithubEvent


class PullRequestEvent(GithubEvent):

    def process(self, request, body):

        pr_link = str(body['pull_request']['url']).replace(
            'https://api.github.com/', '')

        params = {
            'username': body['sender']['login'],
            'user_link': body['sender']['html_url'],
            'pull_request_number': str(body['pull_request']['number']),
            'pull_request_link': self.build_redirect_link('github', 'pull_request', pr_link),
            'pull_request_title': body['pull_request']['title'],
            'body': str(body['pull_request']['body']).strip(),
            'repository_name': body['repository']['full_name'],
            'repository_link': body['repository']['html_url'],
        }
        message = False

        if body['action'] == 'opened':
            message = "[⛓]({pull_request_link}) [{username}]({user_link}) opened new" \
                      " pull request [#{pull_request_number} {pull_request_title}]({pull_request_link})" \
                      " in [{repository_name}]({repository_link})"

        if body['action'] == 'edited':
            message = "[⛓]({pull_request_link}) [{username}]({user_link}) edited" \
                      " pull request [#{pull_request_number} {pull_request_title}]({pull_request_link})" \
                      " in [{repository_name}]({repository_link})"

        if body['action'] == 'closed' and body['pull_request']['merged'] is True:
            message = "[⛓]({pull_request_link}) [{username}]({user_link}) merged" \
                      " pull request [#{pull_request_number} {pull_request_title}]({pull_request_link})"

        if body['action'] == 'closed' and body['pull_request']['merged'] is False:
            message = "[⛓]({pull_request_link}) [{username}]({user_link}) closed" \
                      " pull request [#{pull_request_number} {pull_request_title}]({pull_request_link})" \
                      " in [{repository_name}](repository_link)"

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
            'meta_title': '{issue_title} · PR #{issue_number} · {repo}'.format(
                issue_title=api_result['title'], issue_number=str(api_result['number']), repo=repo),
            'meta_summary': api_result['body'].split("\n")[0][0:100],
            'poster_image': api_result['user']['avatar_url'],
            'redirect': api_result['html_url'],
            'status_code': status_code,
        }
        return redirect
