# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import GithubEvent

"""
Triggered when a user is added or removed as a collaborator to a repository,
or has their permissions changed.
"""


class MemberEvent(GithubEvent):
    def process(self, request, body):
        sender_link = body.get('sender', {}).get('html_url').replace('https://github.com/', '')
        user_link = body.get('member', {}).get('html_url').replace('https://github.com/', '')

        params = {
            'username': body.get('member', {}).get('login', ''),
            'user_link': self.build_redirect_link('github', 'member', user_link),
            'sender_name': body.get('sender', {}).get('login', ''),
            'sender_link': self.build_redirect_link('github', 'member', sender_link),
            'repo': body.get('repository', {}).get('full_name'),
        }

        message = "[{username}]({user_link}) joined the {repo} organisation"

        action = body.get('action', 'added')
        if action == 'edited':
            message = "[{sender_name}]({sender_link}) edited " \
                      "permissions from [{username}]({user_link}) at {repo}"

        if action == 'removed':
            message = "[{sender_name}]({sender_link}) removed " \
                      "[{username}]({user_link}) from {repo}"

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
