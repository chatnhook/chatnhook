from random import randint


class BaseEvent:
    def __init__(self, event, config, project_service_config):
        self.config = config
        self.project_service_config = project_service_config

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
        base_url = "{}/redirect".format(self.config['global']['bot_url'])
        return "{base_url}/{service}/{event}/{url}?{anti_cache}".format(
            base_url=base_url,
            service=service,
            event=event,
            url=url,
            anti_cache=anti_cache
        )
