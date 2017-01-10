class BaseProcessor:

    def __init__(self, request, body, event):
        self.event = event
        self.body = body
        self.request = request

    def process(self):
        raise NotImplementedError
