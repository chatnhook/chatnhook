from ..base import BaseAdapter


class GithubAdapter(BaseAdapter):

    @property
    def event(self):
        return self.request.headers['X-GITHUB-EVENT']
