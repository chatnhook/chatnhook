# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class AlertEvent(BaseEvent):
    def process(self, request, body):
        values = body.get('sentry.interfaces.Exception', {}).get('values', {})
        frames = []
        if values:
            value = values[0]
            frames = value.get('stacktrace', {}).get('frames', [])
        if body.get('type', False):
            level = body.get('type', '')[0].upper() + body.get('type', '')[1:]
        else:
            level = 'Error'

        trace = "{level} in *{culprit}*\n".format(culprit=body.get('culprit', ''),
                                                              level=level,
                                                              project=body.get('project_name',''))
        trace += "{message} \n\n*Stacktrace* (most recent call last)\n".format(
            message=body.get('message', ''))
        for frame in frames:
            trace += "File `{file}`, line {line}, in `{method}`\n```python\t{context}```".format(
                file=frame.get('filename', ''),
                line=frame.get('lineno', 0),
                method=frame.get('function'),
                context=frame.get('context_line').strip()
            )

        message = trace  # + "\n\n [View more]({url})".format(url=body.get('url'))

        return {"default": message}
