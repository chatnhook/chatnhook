# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class IncidentResolveEvent(BaseEvent):

    def process(self, request, body):
        payload = self.body['messages'][0]
        incident = payload['data']['incident']
        assignee = incident['assigned_to'][0]
        message = '[{name}]({user_link}) has resolved [#{incident_number} {incident_title}]({incident_link}) ' \
                  'on pagerduty\n'.format(
                      name=assignee['object']['name'],
                      user_link=assignee['object']['html_url'],
                      incident_number=str(incident['incident_number']),
                      incident_title=incident[
                          'trigger_summary_data']['subject'],
                      incident_link=incident['html_url'],
                  )

        return {'default': message}
