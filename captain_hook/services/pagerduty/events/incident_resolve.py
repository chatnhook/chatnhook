# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class IncidentResolveEvent(BaseEvent):
    def process(self, request, body):
        payload = body.get('messages', {})[0]
        incident = payload.get('data', {}).get('incident', {})
        assignee = incident.get('resolved_by_user')
        message = '[{name}]({user_link}) has resolved ' \
                  '[#{incident_number} {incident_title}]({incident_link}) ' \
                  'on pagerduty\n'\
            .format(
                name=assignee.get('name', ''),
                user_link=assignee.get('html_url', ''),
                incident_number=str(incident.get('incident_number', '')),
                incident_title=incident.get('trigger_summary_data', {}).get('subject', ''),
                incident_link=incident.get('html_url', ''))

        return {'default': message}
