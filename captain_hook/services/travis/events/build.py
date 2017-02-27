# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent
import json
import urllib
import datetime


class BuildEvent(BaseEvent):
    def process(self):
        payload = json.loads(urllib.unquote(self.body['payload']))

        if payload['result_message'] not in self.config['results']:
            return False

        if payload['branch'] not in self.config['notify_branches']:
            return False

        message = 'Build [{build_number}]({build_url}) -  [{commit}]({compare_url}) of' \
                  ' {repository}@{branch} by {author} {result} in {duration}'

        if payload['pull_request']:
            message = 'Build [{build_number}]({build_url}) [{commit}]({compare_url}) of {repository}@{branch} ' \
                      'in PR [{pull_request}]({pull_request_url}) by {author} {result} in {duration}'

        icon = '⚒'

        if payload['result_message'] == 'Pending':
            icon = '🕛'
        if payload['result_message'] == 'Passed':
            icon = '✔'
        if payload['result_message'] == 'Fixed':
            icon = '🎉'
        if payload['result_message'] == 'Broken':
            icon = '💥'
        if payload['result_message'] == 'Failed':
            icon = '💣'
        if payload['result_message'] == 'Still Failing':
            icon = '💣'
        if payload['result_message'] == 'Errored':
            icon = '❌'

        message = icon + ' ' + message.format(
            build_number=payload['number'],
            build_url=payload['build_url'],
            commit=payload['commit'][0:7],
            compare_url=payload['compare_url'],
            repository=payload['repository']['owner_name'] + '/' + payload['repository']['name'],
            branch=payload['branch'],
            author=payload['committer_name'],
            result=payload['result_message'].lower(),
            duration=str(datetime.timedelta(seconds=payload['duration'])),
            pull_request_url=payload['state'],
            pull_request='#' + str(payload['pull_request_number']) + ' ' + str(payload['pull_request_title']),
        )

        return {'default': message}
