from __future__ import absolute_import
from ..base import BaseService


class BitbucketService(BaseService):
    @classmethod
    def get_event(self, request, body):
        return request.headers['x-event-key'].replace(':', '_')

    def get_service_project_config_model(self):
        desc = 'This is the global secret, and will be used at all projects.<br />' \
               'Unless configured on project level'
        return [
            {
                'name': 'notify_branches',
                'label': 'Notify branches',
                'type': 'array',
                'description': ''
            }
        ]
