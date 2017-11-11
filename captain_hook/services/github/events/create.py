# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import GithubEvent

"""
Represents a created repository, branch, or tag.

Note: webhooks will not receive this event for created repositories.
Additionally, webhooks will not receive this event for tags if more than
three tags are pushed at once.
"""


class CreateEvent(GithubEvent):
    def process(self, request, body):
        r_link = str(body.get('repository', {}).get('url', '')).replace(
            'https://api.github.com/', '')
        params = {
            'username': body.get('sender', {}).get('login', ''),
            'user_link': body.get('sender', {}).get('html_url', ''),
            'repository_name': body.get('repository', {}).get('full_name', ''),
            'repository_link': self.build_redirect_link('github', 'create', r_link),
            'what': body.get('ref_type', ''),
            'name': body.get('ref', ''),
        }
        message = '[⚒]({repository_link}) [{username}]({user_link}) created {what} {name}' \
                  ' in [{repository_name}]({repository_link})'

        return {"default": message.format(**params)}

    def get_redirect(self, request, event, params):
        redirect = {
            'meta_title': '',
            'meta_summary': '',
            'poster_image': '',
            'redirect': 'https://github.com/' + params,
            'status_code': 404
        }
        return redirect
