from __future__ import absolute_import
from ..base import BaseService


class PagerdutyService(BaseService):
    def get_event(self, request, body):
        event = body['messages'][0]['type']
        return event.replace('.', '_')
