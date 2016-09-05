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
from django.utils import translation
from django.conf import settings
from django.core import serializers

import djclick as click
import sys
from flier.utils import echo
from flier.smtp.tasks import save_inbound
from flier.smtp import models
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
def ls_domain(ctx, limit, **kwargs):
    q = dict((k, v) for k, v in kwargs.items() if v)
    instances = models.Domain.objects.filter(**q)[:limit]
    echo(serializers.serialize('json', instances))


@main.command()
@click.option('--id', '-i')
@click.option('--limit', '-l', default=20)
@click.pass_context
def ls_sender(ctx, limit, **kwargs):
    q = dict((k, v) for k, v in kwargs.items() if v)
    instances = models.Sender.objects.filter(**q)[:limit]
    echo(serializers.serialize('json', instances))


@main.command()
@click.argument('transport')
@click.argument('sender')
@click.argument('recipient')
@click.argument('original_recipient')
@click.pass_context
def bounce(ctx, transport, sender, recipient, original_recipient):
    '''
        http://www.postfix.org/pipe.8.html
    '''

    if sys.stdin.isatty():
        #: no stdin
        logger.warn('no stdin')
        return

    save_inbound(
        transport, sender, recipient, original_recipient,
        ''.join(sys.stdin.read()),          # raw_message
    )


@main.command()
@click.argument('id')
@click.pass_context
def process_message(ctx, id):
    from flier.smtp.models import Message
    for m in Message.objects.filter(id__in=id):
        m.process_message()


@main.command()
@click.argument('path')
@click.pass_context
def process_drop_mail(ctx, path):
    from flier.smtp.tasks import process_drop_mail
    echo(u"{{ msg }}", msg=process_drop_mail(path))


@main.command()
@click.pass_context
def process_drop(ctx):
    from flier.smtp.tasks import process_drop
    echo(u"{{ msg }}", msg=process_drop())
