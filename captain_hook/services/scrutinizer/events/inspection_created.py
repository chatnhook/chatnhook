# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class InspectionCreatedEvent(BaseEvent):
    def process(self, request, body):
        branch = body.get('metadata', {}).get('branch')
        if branch not in self.project_service_config.get('notify_branches'):
            return False

        if 'inspection.created' not in self.project_service_config.get('events'):
            return False

        inspection = body.get('uuid', '').split('-')[-1]
        inspection_link = 'https://scrutinizer-ci.com' + body.get('_links', {}) \
            .get('self', {}).get('href').replace(
            '/api/repositories', '')
        repo_link = body.get('_embedded', {}).get('repository', {}).get('login', '') + '/' + \
            body.get('_embedded', {}).get('repository', {}).get('name')
        commit = body.get('metadata', {}).get('source_reference', '')[0:7].replace('[', '\[')

        message = '⚒ Inspection [{inspection}]({inspection_url}) ' \
                  '*created* for {repository}@{branch}\n' \
                  'Commits: \n' \
                  '- {commit} - {commit_msg}'

        message = message.format(
            inspection=inspection,
            inspection_url=inspection_link,
            branch=body.get('metadata', {}).get('branch', ''),
            commit=commit,
            repository=repo_link,
            commit_msg=body.get('metadata', {}).get('title', ''))

        return {"default": message}
