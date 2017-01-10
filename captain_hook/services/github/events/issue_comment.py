from ...base.events import BaseEvent


class IssueCommentEvent(BaseEvent):

    def process(self):
        return self.event
