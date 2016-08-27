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
@click.option('--id', '-i', multiple=True)
@click.pass_context
def ls_mails(ctx, queueing, id):
    ''' list all Mail'''
    mails = queueing and Mail.objects.queueing_set() or Mail.objects.all()
    if id:
        mails = mails.filter(id__in=id)

    for mail in mails:
        echo(u"{{ mail.id }}\t\
{{ opt.app_label }}.{{ opt.object_name }}\t\
{{ mail.get_status_display }}\t\
{{ mail.subject }}\t\
to={{ mail.recipients.count}}\t\
active={{ mail.active_recipients.count}}\t\
{{ mail.due_at|default:'' }}",     # NOQA
             mail=mail, opt=mail.instance._meta)


@main.command()
@click.argument('id')
@click.pass_context
def send_mail(ctx, id):
    '''Send a Mail specified by id '''
    Mail.objects.get(id=id).send()
