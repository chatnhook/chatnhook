# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class ReviewCompleteEvent(BaseEvent):
    def process(self, request, body):
        result = 'No new issues'

        if 'results' in body.get('commit'):
            result = '{issues} new issues. {fixes} issues fixed'.format(
                issues=body.get('commit', {}).get('results', {}).get('new_count', '0'),
                fixes=body.get('commit', {}).get('results', {}).get('fixed_count', '0')
            )

        url = body.get('commit', {}).get('data', {}).get('urls', {}).get('delta', '') \
            .replace('https://www.codacy.com/', '')
        link = self.build_redirect_link('codacy', 'review_complete', url)

        message = "**Codacy** review completed! {result}\n[View]({link})".format(
            result=result,
            link=link
        )

        return {"default": str(message)}

    def get_redirect(self, request, event, params):
        params += '?cid=' + request.args.get('cid').split('?')[0]
        redirect = {
            'meta_title': '',
            'meta_summary': '',
            'poster_image': '',
            'redirect': 'https://www.codacy.com/' + params,
            'status_code': 404
        }
        return redirect
