from __future__ import absolute_import
from ..base import BaseService
import hmac
from hashlib import sha1
from flask import abort
from sys import stderr, hexversion


class GithubService(BaseService):
    @property
    def event(self):
        if self.config['enforce_secret']:
            header_signature = self.request.headers.get('X-Hub-Signature')
            if header_signature is None:
                abort(403)
            sha_name, signature = header_signature.split('=')
            if sha_name != 'sha1':
                abort(501)
            # HMAC requires the key to be bytes, but data is string
            mac = hmac.new(str(self.config['enforce_secret']), msg=self.request.data, digestmod=sha1)

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

        return self.request.headers['X-GITHUB-EVENT']
