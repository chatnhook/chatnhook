# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import BitbucketEvent


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
