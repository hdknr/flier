# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from pycommand.djcommand import Command, SubCommand
# from bs4 import BeautifulSoup as Soup

# import sys
import logging

log = logging.getLogger('flier')


class Command(Command):

    class ListSender(SubCommand):
        name = "ls_sender"
        description = _("List Senders")
        args = [
        ]

        def run(self, params, **options):
            from flier.models import Sender
            for sender in Sender.objects.all():
                print sender.id, sender

    class MailTo(SubCommand):
        name = "mail_to"
        description = _("Create and send a mail message")
        args = [
            (('id',), dict(nargs=1, type=int, help="Snder ID")),
            (('subject',), dict(nargs=1, help="Mail Subject")),
            (('body',), dict(nargs=1, help="Mail Body")),
            (('to',), dict(nargs='*', help="Recipiets Address")),
        ]

        def run(self, params, **options):
            from flier.models import Sender
            recipient = Sender.objects.get(
                id=params.id[0]).create_recipient(address=params.to[0])

            recipient.create_message(
                subject=params.subject[0],
                body=params.body[0],).send()
