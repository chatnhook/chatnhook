# -*- coding: utf-8 -*-
from __future__ import absolute_import
from ...base.events import BaseEvent


class BuildCompleteEvent(BaseEvent):
    def process(self, request, body):
        repo = body.get('vcs_url', {}).split('/')[-2:]
        repo = '/'.join(repo)
        repo_url = self.build_redirect_link('circleci', 'build_complete', repo)
        message = '[CircleCI] inspection on [{repo}]({repo_url})@{branch} {outcome} \n'.format(
            repo=repo,
            branch=body.get('branch'),
            outcome=body.get('outcome'),
            repo_url=repo_url
        )

        s = 1
        for step in body.get('steps'):
            message += '{step} of {stepTotal} - {name}\n'.format(
                step=s,
                stepTotal=len(body.get('steps')),
                name=step.get('name'),
            )
            for action in step.get('actions'):
                icon = '✔'
                if action.get('status') != 'success':
                    icon = '❌'
                message += '- {status} {name} {time}ms\n'.format(
                    status=icon,
                    name=action.get('name'),
                    time=action.get('time')
                )
            message += '\n'
            s += 1
        return {"default": str(message)}

    def get_redirect(self, request, event, params):
        redirect = {
            'meta_title': '',
            'meta_summary': '',
            'poster_image': '',
            'redirect': 'https://github.com/' + params,
            'status_code': 404
        }
        return redirect
