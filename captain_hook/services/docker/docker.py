from __future__ import absolute_import
from ..base import BaseService


class DockerService(BaseService):

    @property
    def event(self):
        return 'push' #docker hub only has push event
