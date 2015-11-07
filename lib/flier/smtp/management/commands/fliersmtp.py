# -*- coding: utf-8 -*-
'''

mail.cf(define transport for accepting domains):

    ::

        default_transport=jail

maser.cf(define transport handler script):

    ::

        jail unix  -   n    n   -   -   pipe
          flags=FDRq user=vagrant argv=/bin/inbound.sh jail
            $sender $recipient $original_recipient

inbound.sh(save to Message models):

    ::

        #!/bin/sh
        PY=/home/vagrant/.anyenv/envs/pyenv/versions/venv/bin/python
        MN=/home/vagrant/projects/sample/web/manage.py

        $PY $MN fliersmtp bounce $1 $2

Ubuntu:

- https://help.ubuntu.com/community/PostfixBasicSetupHowto

    ::

        sudo apt-get install postfix mailutils

'''

from django.utils.translation import ugettext_lazy as _
from pycommand.djcommand import Command, SubCommand
# from bs4 import BeautifulSoup as Soup

import sys
import logging

from flier.smtp.tasks import save_inbound

log = logging.getLogger('emailsmtp')


class Command(Command):

    class Bounce(SubCommand):
        '''
            http://www.postfix.org/pipe.8.html
        '''

        name = "bounce"
        description = "bounce by incoming mail"
        args = [
            (('transport',), dict(nargs=1, help="Transport Name")),
            (('sender',), dict(nargs=1, help="Sender Address")),
            (('recipient',), dict(nargs=1, help="Recipient Address")),
            (('original_recipient',),
             dict(nargs=1, help="Original Recipient Address")),
        ]

        def run(self, params, **options):
            ''' read stdin and save it to `flier.smtp.models.Message`
            '''

            if sys.stdin.isatty():
                #: no stdin
                log.warn('no stdin')
                return

            save_inbound(
                params.transport[0],
                params.sender[0],
                params.recipient[0],
                params.original_recipient[0],
                ''.join(sys.stdin.read()),          # raw_message
            )

    class ProcessMessage(SubCommand):

        name = "process_message"
        description = _("Process a Message Object")
        args = [
            (('id',), dict(nargs=1, help="Transport Name")),
        ]

        def run(self, params, **options):
            from flier.smtp.models import Message
            for m in Message.objects.filter(id__in=params.id):
                m.process_message()

    class ProcessDropMail(SubCommand):

        name = "process_drop_mail"
        description = _("Process a Dropped Message")
        args = [
            (('path',), dict(nargs='*', help="Mail Message File")),
        ]

        def run(self, params, **options):
            from flier.smtp.tasks import process_drop_mail
            for path in params.path:
                print process_drop_mail(path)

    class ProcessDrop(SubCommand):

        name = "process_drop"
        description = _("Process a Dropped Message")
        args = []

        def run(self, params, **options):
            from flier.smtp.tasks import process_drop
            print "mails :", process_drop()
