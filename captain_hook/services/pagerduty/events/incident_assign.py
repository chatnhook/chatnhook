# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class IncidentAssignEvent(BaseEvent):
    def process(self):
        message = False
        return {'default': message}
