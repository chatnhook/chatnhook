# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class InspectionCanceledEvent(BaseEvent):
    def process(self, request, body):

        if body['metadata']['branch'] not in self.config['notify_branches']:
            return False

        if 'inspection.canceled' not in self.config['events']:
            return False

        inspection = body['uuid'].split('-')[-1]
        inspection_link = 'https://scrutinizer-ci.com' + body['_links']['self']['href'].replace(
            '/api/repositories', '')
        commit = body['metadata']['source_reference'][0:7].replace('[', '\[')
        repo_link = body['_embedded']['repository']['login'] + '/' + \
            body['_embedded']['repository']['name']

        message = '❌ Inspection [{inspection}]({inspection_url})' \
                  ' *canceled* for {repository}@{branch}\n' \
            .format(
                inspection=inspection,
                inspection_url=inspection_link,
                repository=repo_link,
                branch=body['metadata']['branch'],
                commit=commit,
                commit_msg=body['metadata']['title'])

        return {"default": message}
