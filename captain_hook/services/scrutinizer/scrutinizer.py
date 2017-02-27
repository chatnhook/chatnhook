from __future__ import absolute_import
from ..base import BaseService


class ScrutinizerService(BaseService):

    @property
    def event(self):
        return self.request.headers['X-Scrutinizer-Event'].replace('.', '_')
