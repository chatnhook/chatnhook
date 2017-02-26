# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class PushEvent(BaseEvent):

    def process(self):
        repo = self.body['repository']['repo_name']
        message = '[🐳] Docker image {repo}:{tag} updated'.format(tag=self.body['push_data']['tag'], repo=repo)
        return {"default": str(message)}