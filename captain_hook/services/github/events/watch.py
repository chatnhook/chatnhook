# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import GithubEvent

"""
The WatchEvent is related to starring a repository, not watching. See this API blog post for an explanation.

The event’s actor is the user who starred a repository, and the event’s repository is the repository that was starred.
"""


class WatchEvent(GithubEvent):
	def process(self, request, body):
		user_link = body['sender']['html_url'].replace(
			'https://github.com/', '')
		repo_link = body['repository'][
			'html_url'].replace('https://github.com/', '')

		params = {
			'username': body['sender']['login'],
			'user_link': self.build_redirect_link('github', 'release', user_link),
			'repository_name': body['repository']['full_name'],
			'repository_link': self.build_redirect_link('github', 'release', repo_link),
		}
		message = False
		if body['action'] == 'started':
			message = "❤ [{username}]({user_link}) starred [{repository_name}]({repository_link})"
			message = message.format(**params)

		return {"default": str(message)}

	def get_redirect(self, request, event, params):
		redirect = {
			'meta_title': '',
			'meta_summary': '',
			'poster_image': '',
			'redirect': 'https://github.com/' + params,
			'status_code': 404
		}
		return redirect
