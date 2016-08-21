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
@click.option('--queueing', '-q', is_flag=True)
@click.pass_context
def ls_mails(ctx, queueing):
    ''' list mails'''
    from flier.mails.models import Mail
    mails = queueing and Mail.objects.queueing_set() or Mail.objects.all()
    for mail in mails:
        echo(u"{{ mail.id }}:{{ mail.sender }}:{{ mail.subject}}:{{ mail.due_at|default:'' }}",     # NOQA
             mail=mail)
