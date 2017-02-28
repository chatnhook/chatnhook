from __future__ import absolute_import
from ..base import BaseService


class DockerService(BaseService):

    def get_event(self, request, body):
        return 'push'  # docker hub only has push event
