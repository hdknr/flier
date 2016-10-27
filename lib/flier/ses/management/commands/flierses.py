# -*- coding: utf-8 -*-
from django.utils import translation
from django.conf import settings
from django.core import serializers

import djclick as click
from flier.utils import echo
from flier.ses import models
from logging import getLogger
import json

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
def services(ctx, limit, **kwargs):
    q = dict((k, v) for k, v in kwargs.items() if v)
    instances = models.Service.objects.filter(**q)[:limit]
    echo(serializers.serialize('json', instances))


@main.command()
@click.argument('id')
@click.pass_context
def service_addresses(ctx, id):
    '''Fetch a list of the email addresses that have been verified
    (boto.ses.list_verified_email_addresses)
    '''
    service = models.Service.objects.get(id=id)
    echo(json.dumps(service.list_verified_email_addresses()))


@main.command()
@click.option('--id', '-i')
@click.option('--limit', '-l', default=20)
@click.pass_context
def sources(ctx, limit, **kwargs):
    q = dict((k, v) for k, v in kwargs.items() if v)
    instances = models.Source.objects.filter(**q)[:limit]
    echo(serializers.serialize('json', instances))


@main.command()
@click.argument('id')
@click.argument('address')
@click.pass_context
def verify_address(ctx, id, address):
    '''Verifies an email address.
    This action causes a confirmation email message
    to be sent to the specified address.
    (boto.ses.verify_email_address)
    '''
    source = models.Source.objects.get(id=id)
    echo(json.dumps(source.verify_address(address)))


@main.command()
@click.argument('id')
@click.pass_context
def create_topic(ctx, id):
    source = models.Source.objects.get(id=id)
    source.create_topic('Bounce')
    source.create_topic('Complaint')


@main.command()
@click.argument('id')
@click.argument('to')
@click.argument('subject')
@click.argument('message')
@click.pass_context
def sendmail(ctx, id, to, subject, message):
    source = models.Source.objects.get(id=id)
    recipient = source.create_recipient(to)
    message = recipient.create_message(subject, message)
    message.send()
