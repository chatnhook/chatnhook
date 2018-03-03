import time
class BotStats():
    stats = {
        'messages': {},
        'webhooks': {},
        'redirects': {},
        'uptime': 0
    }

    def __init__(self):
        self.start_time = time.time()

    def count_message(self, service):
        if service in self.stats['messages']:
            self.stats['messages'][service] = self.stats['messages'][service] + 1

        if service not in self.stats['messages']:
            self.stats['messages'][service] = 1

    def count_webhook(self, service, event=''):
        if service in self.stats['webhooks']:
            if event in self.stats['webhooks'][service]:
                self.stats['webhooks'][service][event] += 1

        if service not in self.stats['webhooks']:
            self.stats['webhooks'][service] = {}

        if event not in self.stats['webhooks'][service]:
            self.stats['webhooks'][service][event] = 1

    def count_redirect(self, service):
        if service in self.stats['redirects']:
            self.stats['redirects'][service] += 1

        if service not in self.stats['redirects']:
            self.stats['redirects'][service] = 1

    def get_stats(self):
        self.stats['uptime'] = round(time.time() - self.start_time)
        return self.stats
