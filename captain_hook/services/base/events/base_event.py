class BaseEvent:

    def __init__(self, request, body, event, config):
        self.event = event
        self.body = body
        self.request = request
        self.config = config

    def process(self):
        raise NotImplementedError
