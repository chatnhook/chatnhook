from __future__ import absolute_import
from ..base import BaseService


class SlackService(BaseService):
    def get_event(self, request, body):
        return 'message'
