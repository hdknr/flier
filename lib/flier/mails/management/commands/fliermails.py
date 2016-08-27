# -*- coding: utf-8 -*-
from django.utils import translation, timezone
from django.conf import settings
from django.core import serializers

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


@main.command()
@click.argument('id')
@click.argument('status')
@click.pass_context
def set_status(ctx, id, status):
    '''force change status'''
    mail = Mail.objects.filter(id=id).first()

    if not mail:
        echo(u"No mail for {{ id }}", id=id)
        return

    code = getattr(Mail, 'STATUS_' + status.upper(), -1)
    if code == -1:
        options = ['DISABLED', 'QUEUED', 'SENDING', 'SENT']
        echo(u"status must be in {{ o|safe }}", o=str(options))
        return

    mail.status = code
    mail.sent_at = timezone.now() if code == Mail.STATUS_SENT else None
    mail.save()


@main.command()
@click.argument('id')
@click.argument('address', nargs=-1)
@click.pass_context
def recipients(ctx, id, address):

    mail = Mail.objects.filter(id=id).first()

    if not mail:
        echo(u"No mail for {{ id }}", id=id)
        return

    echo(serializers.serialize(
         'json', mail.recipients.filter(to__address__in=address)))
