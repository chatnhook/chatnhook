from __future__ import absolute_import
from ..base import BaseService


class TravisService(BaseService):

    def get_event(self, request, body):
        return 'build'
