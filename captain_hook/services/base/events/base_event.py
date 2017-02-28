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
        anti_cache = str(randint(0, 999))
        base_url = "{}/redirect".format(self.config['general']['bot_url'])
        return "{base_url}/{service}/{event}/{url}?{anti_cache}"
