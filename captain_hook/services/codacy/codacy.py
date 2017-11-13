from __future__ import absolute_import
from ..base import BaseService


class CodacyService(BaseService):
    def get_event(self, request, body):
        return 'review_complete'
