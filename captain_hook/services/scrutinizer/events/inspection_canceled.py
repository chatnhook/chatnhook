# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class InspectionCanceledEvent(BaseEvent):
    def process(self):

        if self.body['metadata']['branch'] not in self.config['notify_branches']:
            return False

        if 'inspection.canceled' not in self.config['events']:
            return False

        inspection = self.body['uuid'].split('-')[-1]
        inspection_link = 'https://scrutinizer-ci.com' + self.body['_links']['self']['href'].replace(
            '/api/repositories', '')
        commit = self.body['metadata']['source_reference'][0:7].replace('[', '\[')

        message = '❌ Inspection [{inspection}]({inspection_url}) *canceled* for {repository}@{branch}\n'.format(
            inspection=inspection,
            inspection_url=inspection_link,
            repository=self.body['_embedded']['repository']['login'] + '/' + self.body['_embedded']['repository'][
                'name'],
            branch=self.body['metadata']['branch'],
            commit=commit,
            commit_msg=self.body['metadata']['title']
        )

        return {"default": message}
