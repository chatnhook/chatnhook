from ...base.processors import BaseProcessor


class IssueCommentProcessor(BaseProcessor):

    def process(self):
        return self.event
