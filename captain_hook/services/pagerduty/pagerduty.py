from __future__ import absolute_import
from ..base import BaseService


class PagerdutyService(BaseService):

    @property
    def event(self):
        event = self.body['messages'][0]['type']
        return event.replace('.','_')
