# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import GithubEvent

"""
Triggered when a commit comment is created.
"""


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
		s = api_result['url'].split('/')
		repo = s[4] + '/' + s[5]
		title = '{username} commented on commit `{commit}` · {repo}'
		redirect = {
			'meta_title': title.format(username=api_result['user']['login'],
									   commit=api_result['commit_id'][:7],
									   repo=repo),
			'meta_summary': api_result['body'].split("\n")[0][0:100],
			'poster_image': api_result['user']['avatar_url'],
			'redirect': api_result['html_url'],
			'status_code': status_code,
		}
		return redirect
