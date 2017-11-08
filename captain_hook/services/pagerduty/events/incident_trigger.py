# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class IncidentTriggerEvent(BaseEvent):
    def process(self, request, body):
        payload = body['messages'][0]
        incident = payload['data']['incident']
        assignee = incident['assigned_to'][0]
        message = 'New incident created on pagerduty \n' \
                  '[#{incident_number} {incident_title}]({incident_link}) Urgency: *{urgency}* \n' \
                  'Assigned to [{name}]({user_link})'.format(
            name=assignee['object']['name'],
            user_link=assignee['object']['html_url'],
            incident_number=str(incident['incident_number']),
            incident_title=incident[
                'trigger_summary_data']['subject'],
            incident_link=incident['html_url'],
            urgency=incident['urgency']
        )

        return {'default': message}
