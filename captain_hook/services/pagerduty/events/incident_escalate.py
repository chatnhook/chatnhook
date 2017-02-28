# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class IncidentEscalateEvent(BaseEvent):

    def process(self, request, body):
        payload = body['messages'][0]
        incident = payload['data']['incident']
        assignee = incident['assigned_to'][0]
        message = '[#{incident_number} {incident_title}]({incident_link}) has been escalated' \
                  ' to [{name}]({user_link}) on pagerduty\n'.format(
                      name=assignee['object']['name'],
                      user_link=assignee['object']['html_url'],
                      incident_number=str(incident['incident_number']),
                      incident_title=incident[
                          'trigger_summary_data']['subject'],
                      incident_link=incident['html_url']
                  )
        return {'default': message}
