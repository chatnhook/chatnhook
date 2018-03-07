from __future__ import absolute_import
from ..base import BaseService


class ZabbixService(BaseService):
    def get_event(self, request, body):
        return 'issue'
