from __future__ import absolute_import
from ..base import BaseService


class TravisService(BaseService):

    @property
    def event(self):
        return 'build'
