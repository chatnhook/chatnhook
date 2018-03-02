# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class InspectionCanceledEvent(BaseEvent):
    def process(self, request, body):
        branch = body.get('metadata', {}).get('branch')
        if branch not in self.project_service_config.get('notify_branches'):
            return False

        if 'inspection.canceled' not in self.project_service_config.get('events'):
            return False

        inspection = body.get('uuid', '').split('-')[-1]
        inspection_link = 'https://scrutinizer-ci.com' + body.get('_links', {}) \
            .get('self', {}).get('href').replace(
            '/api/repositories', '')

        commit = body.get('metadata', {}).get('source_reference', '')[0:7].replace('[', '\[')
        repo_link = body.get('_embedded', {}).get('repository', {}).get('login', '') + '/' + \
            body.get('_embedded', {}).get('repository', {}).get('name')

        message = '❌ Inspection [{inspection}]({inspection_url})' \
                  ' *canceled* for {repository}@{branch}\n' \
            .format(
                inspection=inspection,
                inspection_url=inspection_link,
                repository=repo_link,
                branch=body.get('metadata', {}).get('branch', ''),
                commit=commit,
                commit_msg=body.get('metadata', {}).get('title', ''))

        return {"default": message}
