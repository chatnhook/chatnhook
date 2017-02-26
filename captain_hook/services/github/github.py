from __future__ import absolute_import
from ..base import BaseService


class GithubService(BaseService):

    @property
    def event(self):
        return self.request.headers['X-GITHUB-EVENT']
