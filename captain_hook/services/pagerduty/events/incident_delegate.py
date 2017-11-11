# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class IncidentDelegateEvent(BaseEvent):
    def process(self, request, body):
        payload = body.get('messages')[0]
        incident = payload.get('data', {}).get('incident')
        assignee = incident.get('assigned_to')[0]
        message = '[#{incident_number} {incident_title}]({incident_link}) ' \
                  'has been delegated to [{name}]({user_link}) on pagerduty\n'\
            .format(
                name=assignee.get('object', {}).get('name', ''),
                user_link=assignee.get('object', {}).get('html_url', ''),
                incident_number=str(incident.get('incident_number', '')),
                incident_title=incident.get('trigger_summary_data', {}).get('subject', ''),
                incident_link=incident.get('html_url', ''))
        return {'default': message}
