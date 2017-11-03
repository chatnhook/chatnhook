# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import GithubEvent

"""
Triggered when a repository's label is created, edited, or deleted.
"""


class LabelEvent(GithubEvent):
	def process(self, request, body):
		return {"default": ''}

	def get_redirect(self, request, event, params):
		redirect = {
			'meta_title': '',
			'meta_summary': '',
			'poster_image': '',
			'redirect': 'https://github.com/' + params,
			'status_code': 404
		}
		return redirect
