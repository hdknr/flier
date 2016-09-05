# -*- coding: utf-8 -*-
from django.utils import translation
from django.conf import settings
from django.core import serializers
import djclick as click
from flier.utils import echo
from flier import validators, models
from logging import getLogger

logger = getLogger('flier')
translation.activate(settings.LANGUAGE_CODE)


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    pass


@main.command()
@click.option('--id', '-i')
@click.option('--limit', '-l', default=20)
@click.pass_context
def senders(ctx, limit, **kwargs):
    q = dict((k, v) for k, v in kwargs.items() if v)
    instances = models.Sender.objects.filter(**q)[:limit]
    echo(serializers.serialize('json', instances))


@main.command()
@click.option('--id', '-i')
@click.option('--limit', '-l', default=20)
@click.pass_context
def status(ctx, limit, **kwargs):
    q = dict((k, v) for k, v in kwargs.items() if v)
    instances = models.RecipientStatus.objects.filter(**q)[:limit]
    echo(serializers.serialize('json', instances))


@main.command()
@click.option('--message_id', '-m')
@click.option('--sender', '-s')
@click.option('--status__code')
@click.option('--status')
@click.option('--key', '-k')
@click.option('--content_type', '-c')
@click.option('--object_id', '-o')
@click.option('--limit', '-l', default=20)
@click.pass_context
def recipients(ctx, limit, **kwargs):
    q = dict((k, v) for k, v in kwargs.items() if v)
    instances = models.Recipient.objects.filter(**q)[:limit]
    echo(serializers.serialize('json', instances))


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


@main.command()
@click.argument('addrs', nargs=-1)
@click.pass_context
def validate_email(ctx, addrs):
    for a in addrs:
        echo(u"{{check.0}} : {{check.1}}",
             check=validators.validate_email.check(a))
