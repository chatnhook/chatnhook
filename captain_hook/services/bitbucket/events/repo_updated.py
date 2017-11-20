# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import BitbucketEvent
import itertools
"""
Triggered on a push to a repository branch.
Branch pushes and repository tag pushes also trigger webhook push events.

Note: The webhook payload example following the table differs significantly
from the Events API payload described in the Github API. Among other differences,
the webhook payload includes both sender and pusher objects.
Sender and pusher are the same user who initiated the push event,
but the sender object contains more detail.
"""


class RepoUpdatedEvent(BitbucketEvent):
    def process(self, request, body):
        return {"default": ''}

    def get_redirect(self, request, event, params):
        redirect = {
            'meta_title': '',
            'meta_summary': '',
            'poster_image': '',
            'redirect': 'https://bitbucket.org/' + params,
            'status_code': 404
        }
        return redirect
