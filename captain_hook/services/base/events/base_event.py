class BaseEvent:

    def __init__(self, event, config):
        self.config = config

    def process(self, request, body):
        raise NotImplementedError
