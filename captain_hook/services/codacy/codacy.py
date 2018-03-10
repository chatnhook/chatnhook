from __future__ import absolute_import
from ..base import BaseService
import os


class CodacyService(BaseService):
    @classmethod
    def get_event(self, request, body):
        return 'review_complete'

    def get_config_template(self):
        dir = os.path.dirname(os.path.realpath(__file__))
        contents = open(dir + '/service.html').read()
        return contents
