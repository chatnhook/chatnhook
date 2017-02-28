from random import randint
import requests
from json import loads


class BaseEvent:
    def __init__(self, event, config):
        self.config = config

    def process(self, request, body):
        raise NotImplementedError

    def get_redirect(self, request, event, params):
        redirect = {
            'meta_title': '',
            'meta_summary': '',
            'poster_image': '',
            'redirect': '',
            'status_code': 200
        }
        return redirect

    def build_redirect_link(self, service, event, url):
        # Append a random number as query param to disable caching
        antiCache = str(randint(0, 999))
        base = self.config['global_config']['boturl'] + '/redirect/'
        url = base + service + '/' + event + '/' + url + '?' + antiCache
        return url

    # @TODO move this to a util lib in github service
    def gh_api(self, url):
        if 'https://api.github.com/' not in url:
            url = 'https://api.github.com/' + url

        response = requests.get(url=url)
        try:
            result = loads(response.text)
        except TypeError:
            result = False
        return result
