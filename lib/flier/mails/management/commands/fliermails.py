# -*- coding: utf-8 -*-
from django.utils import translation
from django.conf import settings

import djclick as click
from flier.utils import echo
from flier.mails.models import Mail
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
    ''' list all Mail'''
    mails = queueing and Mail.objects.queueing_set() or Mail.objects.all()
    for mail in mails:
        echo(u"{{ mail.id }}:\
{{ opt.app_label }}.{{ opt.object_name }}:\
{{ mail.subject}}:\
to={{ mail.mailrecipient_set.count}}:\
{{ mail.due_at|default:'' }}",     # NOQA
             mail=mail, opt=mail.instance._meta)


@main.command()
@click.argument('id')
@click.pass_context
def send_mail(ctx, id):
    '''Send a Mail specified by id '''
    Mail.objects.get(id=id).send()
