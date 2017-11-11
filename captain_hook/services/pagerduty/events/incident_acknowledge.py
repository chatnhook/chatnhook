# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class IncidentAcknowledgeEvent(BaseEvent):
    def process(self, request, body):
        payload = body.get('messages', {})[0]
        acknowledger = payload.get('data', {}).get('incident', {}).get('acknowledgers', {})[0]\
            .get('object')
        incident = payload.get('data', {}).get('incident', {})

        message = '[{name}]({user_link}) has acknowledged incident' \
                  ' [#{incident_number} {incident_title}]({incident_link})'\
            .format(
                name=acknowledger.get('name'),
                user_link=acknowledger.get('html_url', ''),
                incident_number=str(incident.get('incident_number', '')),
                incident_title=incident.get('trigger_summary_data', {}).get('subject', ''),
                incident_link=incident.get('html_url', ''))

        return {'default': message}
