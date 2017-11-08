# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import GithubEvent

"""
Represents an attempted build of a GitHub Pages site, whether successful or not.

Triggered on push to a GitHub Pages enabled branch (gh-pages for project pages, master for user and organization pages).
"""


class PageBuildEvent(GithubEvent):
    def process(self, request, body):
        return {"default": ''}

    def get_redirect(self, request, event, params):
        redirect = {
            'meta_title': '',
            'meta_summary': '',
            'poster_image': '',
            'redirect': 'https://github.com/' + params,
            'status_code': 404
        }
        return redirect
