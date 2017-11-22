from __future__ import absolute_import
from ..base import BaseService


class BitbucketService(BaseService):
    @classmethod
    def get_event(self, request, body):
        return request.headers['x-event-key'].replace(':', '_')
