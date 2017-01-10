from ...base.processors.base import BaseProcessor


class IssueCommentProcessor(BaseProcessor):

    def process(self):
        return self.event
