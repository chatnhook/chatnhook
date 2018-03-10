import json
from time import time
import uuid


class WebhookInspector():
    inspections = []

    def __init__(self):
        pass

    def inspect(self, path, req):
        raw_body = req.get_data()
        headers = []
        for key, val in enumerate(req.headers.to_list()):
            headers.append({'header': val[0], 'value': val[1]})

        try:
            body = json.loads(req.data)
        except ValueError:
            body = req.form

        guid = uuid.uuid4()
        request = {
            'headers': headers,
            'path': path,
            'timestamp': time(),
            'body': body,
            'method': req.method,
            'body_raw': raw_body,
            'ip': req.remote_addr,
            'guid': guid,
            'type': req.headers.get('Content-Type').replace('application/', '')
        }

        self.inspections.insert(0, request)
        return True

    def clear_inspections(self):
        self.inspections = []
        return True

    def get_inspection(self, guid):
        for inspection in self.inspections:
            if str(inspection.get('guid')) == str(guid):
                return inspection
        return None

    def get_inspections(self, limit=None):
        if not limit:
            return self.inspections
        else:
            return self.inspections[:limit]
