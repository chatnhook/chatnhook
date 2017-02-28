from __future__ import absolute_import
from ..base import BaseService


class PatreonService(BaseService):

    def get_event(self, request, body):
        return request.headers['X-Patreon-Event'].replace(':', '_')
