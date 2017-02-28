from ...base.events import BaseEvent
import requests
from json import loads


class GithubEvent(BaseEvent):

    def gh_api(self, url):
        if 'https://api.github.com/' not in url:
            url = 'https://api.github.com/' + url

        response = requests.get(url=url)
        try:
            result = loads(response.text)
        except TypeError:
            result = False
        return result
