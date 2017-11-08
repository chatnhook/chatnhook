# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import GithubEvent

"""
Triggered when an issue comment is created, edited, or deleted.
"""


class IssueCommentEvent(GithubEvent):
	def process(self, request, body):
		issue_type = 'issue'
		if 'pull_request' in body['issue']:
			issue_type = 'pull request'

		comment_api_link = str(body['comment']['url']).replace(
			'https://api.github.com/', '')

		params = {
			'username': body['comment']['user']['login'],
			'user_link': body['comment']['user']['html_url'],
			'issue_number': str(body['issue']['number']),
			'comment_link': self.build_redirect_link('github', 'issue_comment', comment_api_link),
			'issue_title': body['issue']['title'].encode('utf-8'),
			'issue_type': issue_type,
			'body': str(body['comment']['body']).split("\n")[0] + '...',
		}

		if body['action'] == 'created':
			message = "[🗨]({comment_link}) [{username}]({user_link}) commented " \
					  "on {issue_type} [#{issue_number} {issue_title}]({comment_link})"
			# message += '```{body}```'
			message = message.format(**params)

		if body['action'] == 'edited':
			message = "[🗨]({comment_link}) [{username}]({user_link}) edited the" \
					  " comment on {issue_type} [#{issue_number} {issue_title}]({comment_link})"
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
		issue = self.gh_api(api_result['issue_url'])
		s = api_result['url'].split('/')
		repo = s[4] + '/' + s[5]
		redirect = {
			'meta_title': '{username} replied · {issue_title} · {issue_type} #{issue_number} · {repo}'.format(
				issue_title=issue['title'].encode('utf-8'), issue_number=str(issue['number']), repo=repo,
				username=api_result['user']['login'],
				issue_type=issue_type),
			'meta_summary': api_result['body'].split("\n")[0][0:100],
			'poster_image': api_result['user']['avatar_url'],
			'redirect': api_result['html_url'],
			'status_code': status_code,
		}
		return redirect
