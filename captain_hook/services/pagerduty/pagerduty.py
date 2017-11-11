from __future__ import absolute_import
from ..base import BaseService


class PagerdutyService(BaseService):
    def get_event(self, request, body):
        event = body.get('messages', {})[0].get('type')
        return event.replace('.', '_')
