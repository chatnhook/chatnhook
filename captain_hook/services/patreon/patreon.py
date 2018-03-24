from __future__ import absolute_import
from ..base import BaseService
from flask import abort
import hmac
from hashlib import md5
from sys import hexversion
class PatreonService(BaseService):
    def get_event(self, request, body):

        key = self.project_service_config.get('settings', {}).get('verification_key', False)
        if not key:
            key = self.config.get('verification_key', False)
        if key:
            if key != request.args.get('verification_key', False):
                return False

        secret = self.project_service_config.get('settings', {}).get('secret', False)
        if secret:
            header_signature = request.headers.get('X-Hub-Signature', '')
            if header_signature is None:
                abort(403)

            sha_name = None
            signature = None
            # HMAC requires the key to be bytes, but data is string
            mac = hmac.new(
                str(secret), msg=request.data, digestmod=md5)

            # Python prior to 2.7.7 does not have hmac.compare_digest
            if hexversion >= 0x020707F0:
                if not hmac.compare_digest(str(mac.hexdigest()), str(signature)):
                    abort(403)
            else:
                # What compare_digest provides is protection against timing
                # attacks; we can live without this protection for a web-based
                # application
                if not str(mac.hexdigest()) == str(signature):
                    abort(403)

        return request.headers.get('X-Patreon-Event').replace(':', '_')

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
            },
            {
                'name': 'secret',
                'label': 'Secret',
                'type': 'text',
                'description': desc
            }
        ]
