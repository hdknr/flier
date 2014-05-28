# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from pycommand.command import Command as PyCommand, SubCommand
#from django.utils.translation import ugettext as _


class Command(BaseCommand, PyCommand):
    managers = ['manage.py', ]

    def run_from_argv(self, argv):
        return self.run(argv)

    class TargetDescription(SubCommand):
        name = "desc_target"
        description = "List Target "
        args = [
            (('id',), dict(nargs=1, type=int, help="target id")),
        ]

        def run(self, params, **options):
            pass
