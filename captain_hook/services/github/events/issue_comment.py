from __future__ import absolute_import
from ...base.events import BaseEvent


class IssueCommentEvent(BaseEvent):

    def process(self):
        return {"telegram": str(self.event)}
