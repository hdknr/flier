# -*- coding: utf-8 -*-
from django.utils import translation
from django.conf import settings
import djclick as click
from flier.utils import echo
from logging import getLogger

logger = getLogger('flier')
translation.activate(settings.LANGUAGE_CODE)


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    pass


@main.command()
@click.pass_context
def ls_sender(ctx):
    from flier.models import Sender
    for sender in Sender.objects.all():
        echo(u"{{ sender.id }} {{ sender }}", sender=sender)


@main.command()
@click.argument('id')
@click.argument('subject')
@click.argument('body')
@click.argument('to', nargs=-1)
@click.pass_context
def mail_to(ctx, id, subject, body, to):
    from flier.models import Sender

    for to_addr in to:
        recipient = Sender.objects.get(id=id).create_recipient(
            address=to_addr)

        recipient.create_message(subject=subject, body=body).send()
