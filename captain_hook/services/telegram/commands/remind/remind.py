# -*- coding: utf-8 -*-
from __future__ import absolute_import
from captain_hook.services.telegram.commands.base import BaseCommand


class RemindCommand(BaseCommand):
    def run(self, args):
        return 'test'
