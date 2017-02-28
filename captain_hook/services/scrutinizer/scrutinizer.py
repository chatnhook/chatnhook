from __future__ import absolute_import
from ..base import BaseService


class ScrutinizerService(BaseService):

    def get_event(self, request, body):
        return request.headers['X-Scrutinizer-Event'].replace('.', '_')
