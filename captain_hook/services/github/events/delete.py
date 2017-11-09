# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import GithubEvent

"""
Represents a deleted branch or tag.

Note: webhooks will not receive this event for tags if more than three tags are deleted at once.
"""


class DeleteEvent(GithubEvent):
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
