from time import time


class Hooklog():
    logged_hooks = []

    def __init__(self):
        pass

    def log_hook(self, project, service, event, comms):
        self.logged_hooks.insert(0, {
            'timestamp': time(),
            'project': project,
            'service': service,
            'event': event,
            'comm_result': comms
        })
        pass

    def get_logged_hooks(self, limit=None):
        if not limit:
            return self.logged_hooks
        else:
            return self.logged_hooks[:limit]