from ...base.events import BaseEvent
import requests
from json import loads


class BitbucketEvent(BaseEvent):
    def bb_api(self, url):
        if 'https://api.bitbucket.org/2.0/' not in url:
            url = 'https://api.bitbucket.org/2.0/' + url

        headers = {
            'User-Agent': 'Hookbot',
        }
        if 'token' in self.config:
            headers['Authorization'] = 'Bearer ' + self.config.get('token')


        response = requests.get(url=url, headers=headers)

        try:
            result = loads(response.text)
        except TypeError:
            result = False

        return result
