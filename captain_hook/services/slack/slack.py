from __future__ import absolute_import
from ..base import BaseService


class SlackService(BaseService):

    @property
    def event(self):
        return 'message'
