from __future__ import absolute_import
from ..base import BaseService


class CircleciService(BaseService):
    @classmethod
    def get_event(self, request, body):
        return 'build_complete'  # circleci only has build complete event
