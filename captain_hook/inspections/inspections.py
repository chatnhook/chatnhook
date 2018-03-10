import json
from time import time
import uuid

class WebhookInspector():
    inspections = []

    def __init__(self):
        pass

    def inspect(self, path, req):

        headers = {}
        for key, val in enumerate(req.headers.to_list()):
            headers[val[0]] = val[1]

        try:
            body = json.loads(req.data)
        except ValueError:
            body = req.form

        uid = uuid.uuid4()
        request = {
            'headers': headers,
            'url': path,
            'timestamp': time(),
            'body': body,
            'ip': req.remote_addr,
            'uid': uid
        }
        self.inspections.insert(0, request)
        return True

    def clear_inspections(self):
        self.inspections = []
        return True

    def get_inspections(self, limit=None):
        if not limit:
            return self.inspections
        else:
            return self.inspections[:limit]
