from __future__ import absolute_import
from ..base import BaseService
import os


class CodacyService(BaseService):
    def get_event(self, request, body):

        key = self.project_service_config.get('settings', {}).get('verification_key', False)
        if not key:
            key = self.config.get('verification_key', False)
        if key:
            if key != request.args.get('verification_key', False):
                return False

        return 'review_complete'

    def get_service_config_model(self):
        desc = 'This is the global verification key, and will be used at all projects.<br />' \
               'Unless configured on project level. <br />' \
               'This will be used to protect your endpoints'
        return [
            {
                'name': 'verification_key',
                'label': 'Verification key',
                'type': 'text',
                'description': desc
            }
        ]

    def get_service_project_config_model(self):
        desc = 'This is the global verification key, and will be used at all projects.<br />' \
               'Unless configured on project level. <br />' \
               'This will be used to protect your endpoints'
        return [
            {
                'name': 'verification_key',
                'label': 'Verification key',
                'type': 'text',
                'description': desc
            }
        ]
