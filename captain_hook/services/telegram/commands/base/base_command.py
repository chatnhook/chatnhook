# -*- coding: utf-8 -*-
from __future__ import absolute_import
from captain_hook.services.base.events import BaseEvent
from pprint import pprint
import json
import importlib


class BaseCommand:
    def __init__(self, config):
        self.config = config

    def run(self, args):
        raise NotImplementedError
