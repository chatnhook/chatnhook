from __future__ import absolute_import
from ..base import BaseService


class PatreonService(BaseService):

    @property
    def event(self):
        return self.request.headers['X-Patreon-Event'].replace(':','_')
