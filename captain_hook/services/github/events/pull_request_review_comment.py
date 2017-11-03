# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import GithubEvent

"""
Triggered when a comment on a pull request's unified diff is created, edited, or deleted (in the Files Changed tab).
"""


class PullRequestReviewCommentEvent(GithubEvent):
	def process(self, request, body):

		comment_api_link = str(body['comment']['url']).replace(
			'https://api.github.com/', '')
		params = {
			'username': body['comment']['user']['login'],
			'user_link': body['comment']['user']['html_url'],
			'pr_comment_link': self.build_redirect_link('github', 'pull_request_review_comment', comment_api_link),
			'pr_number': str(body['pull_request']['number']),
			'pr_title': body['pull_request']['title'],
			'pr_link': body['pull_request']['html_url'],
		}

		message = False
		if body['action'] == 'created':
			message = "[🗨]({pr_comment_link}) [{username}]({user_link}) " \
					  "commented on a file in PR [#{pr_number} {pr_title}]({pr_link})"
			# message += '```{body}```'
			message = message.format(**params)

		if body['action'] == 'edited':
			message = "[🗨]({pr_comment_link}) [{username}]({user_link}) edited " \
					  "the comment on a file in PR [#{pr_number} {pr_title}]({pr_link})"
			# message += '```{body}```'
			message = message.format(**params)

		return {"default": str(message)}

	def get_redirect(self, request, event, params):
		api_result = self.gh_api(params)
		status_code = 200
		if not api_result:
			status_code = 404
		s = api_result['url'].split('/')
		repo = s[4] + '/' + s[5]

		redirect = {
			'meta_title': '{path}:{line} · {repo}'.format(path=api_result['path'],
														  line=str(api_result['position']), repo=repo),
			'meta_summary': api_result['body'].split("\n")[0][0:100],
			'poster_image': api_result['user']['avatar_url'],
			'redirect': api_result['html_url'],
			'status_code': status_code,
		}
		return redirect
