# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class InspectionCompletedEvent(BaseEvent):
    def process(self, request, body):

        if body['metadata']['branch'] not in self.config['notify_branches']:
            return False

        if 'inspection.completed' not in self.config['events']:
            return False

        inspection = body['uuid'].split('-')[-1]
        inspection_link = 'https://scrutinizer-ci.com' + body['_links']['self']['href'].replace(
            '/api/repositories', '')
        commit = body['metadata']['source_reference'][0:7].replace('[', '\[')

        message = '🎉 Inspection [{inspection}]({inspection_url}) *completed* for {repository}@{branch}\n' \
                  'Commits: \n' \
                  '- {commit} - {commit_msg}'

        message = message.format(
            inspection=inspection,
            inspection_url=inspection_link,
            repository=body['_embedded']['repository'][
                           'login'] + '/' + body['_embedded']['repository']['name'],
            branch=body['metadata']['branch'],
            commit=commit,
            commit_msg=body['metadata']['title']
        )

        return {"default": message}
