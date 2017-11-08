# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import GithubEvent

"""
Triggered when a user is added or removed as a collaborator to a repository, or has their permissions changed.
"""


class MemberEvent(GithubEvent):
    def process(self, request, body):
        sender_link = body['sender']['html_url'].replace('https://github.com/', '')
        user_link = body['member']['html_url'].replace('https://github.com/', '')
        repo_link = body['repository']['html_url'].replace('https://github.com/', '')

        params = {
            'username': body['member']['login'],
            'user_link': self.build_redirect_link('github', 'member', user_link),
            'sender_name': body['sender']['login'],
            'sender_link': self.build_redirect_link('github', 'member', sender_link),
            'org_name': body['organization']['login'],
        }

        message = "[{username}]({user_link}) joined the {org_name} organisation"

        action = body.get('action', 'added')
        if action == 'edited':
            message = "[{sender_name}]({sender_link}) edited permissions from [{username}]({user_link}) at {org_name}"

        if action == 'removed':
            message = "[{sender_name}]({sender_link}) removed [{username}]({user_link}) from {org_name}"

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
