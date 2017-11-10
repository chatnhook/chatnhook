# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent
import json
import urllib
import datetime
from pprint import pprint


class BuildEvent(BaseEvent):
    def process(self, request, body):
        payload = json.loads(urllib.unquote(body['payload']))
        if payload['result_message'] not in self.config['results']:
            return {'default': ''}

        if payload['branch'] not in self.config['notify_branches']:
            return {'default': ''}

        message = 'Build [{build_number}]({build_url}) -  [{commit}]({compare_url}) of' \
                  ' {repository}@{branch} by {author} {result} in {duration}'

        if payload.get('pull_request'):
            message = 'Build [{build_number}]({build_url}) [{commit}]({compare_url})' \
                      ' of {repository}@{branch} in PR [{pull_request}]({pull_request_url}) ' \
                      'by {author} {result} in {duration}'

        icon = '⚒'

        if payload.get('result_message') == 'Pending':
            icon = '🕛'
        if payload.get('result_message') == 'Passed':
            icon = '✔'
        if payload.get('result_message') == 'Fixed':
            icon = '🎉'
        if payload.get('result_message') == 'Broken':
            icon = '💥'
        if payload.get('result_message') == 'Failed':
            icon = '💣'
        if payload.get('result_message') == 'Still Failing':
            icon = '💣'
        if payload.get('result_message') == 'Errored':
            icon = '❌'

        message = icon + ' ' + message.format(
            build_number=payload.get('number'),
            build_url=payload.get('build_url'),
            commit=payload.get('commit')[0:7],
            compare_url=payload.get('compare_url'),
            repository=payload.get('repository').get('owner_name') + '/' +
                         payload.get('repository').get('name'),
            branch=payload.get('branch'),
            author=payload.get('committer_name'),
            result=payload.get('result_message').lower(),
            duration=str(datetime.timedelta(seconds=payload.get('duration'))),
            pull_request_url=payload.get('state'),
            pull_request='#' +
                         str(payload.get('pull_request_number')) + ' ' +
                         str(payload.get('pull_request_title')),
        )

        return {'default': message}
