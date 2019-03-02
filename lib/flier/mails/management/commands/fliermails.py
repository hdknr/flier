# -*- coding: utf-8 -*-
from django.utils import translation, timezone
from django.conf import settings
from django.core import serializers

import djclick as click
from flier.utils import echo
from flier.mails.models import Mail, MailTemplate
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
task={{ mail.task_id }}\t\
{{ mail.due_at|default:'' }}",     # NOQA
             mail=mail, opt=mail.instance._meta)


@main.command()
@click.argument('id')
@click.option('--force', '-f', is_flag=True)
@click.pass_context
def send_mail(ctx, id, force):
    '''Send a Mail specified by id '''
    mail = Mail.objects.get(id=id)
    if force:
        mail.status = 'queued'
        mail.sent_at = None
        mail.save()
        mail.recipients.all().delete()
    mail.send()


@main.command()
@click.option('--run', '-r', is_flag=True)
@click.pass_context
def enqueue(ctx, run):
    ''' check queuable Mail, and enqueue them if `--run` is specified '''
    mails = Mail.objects.queueing_set()
    for m in mails:
        if run:
            m.enqueue()
        echo("{{m.id}}: {{m.subject}}:task {{m.task_id}}",  m=m)


@main.command()
@click.argument('id')
@click.pass_context
def prepare_sending(ctx, id):
    '''Send a Mail specified by id '''
    mail = Mail.objects.filter(id=id).first()
    if not mail:
        echo('No Mail for id={{ id }}', id=id)
        return
    if mail.status == 'sending':
        echo('This mail is being processed.')
        return
    mail.instance.prepare_sending()


@main.command(
    help="change Mail status :[{}]".format(
        '|'.join(i[0] for i in Mail.STATUS)))
@click.argument('id')
@click.argument('status')
@click.pass_context
def set_status(ctx, id, status):
    '''force change status'''
    status = status.lower()
    mail = Mail.objects.filter(id=id).first()

    if not mail:
        echo(u"No mail for {{ id }}", id=id)
        return

    mail.status = status
    mail.sent_at = timezone.now() if status == Mail.STATUS_SENT else None
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

    qs = address and mail.recipients.filter(to__address__in=address) \
        or mail.recipients.filter()

    echo(serializers.serialize('json', qs))


@main.command()
@click.argument('template_id')
@click.argument('address', nargs=-1)
@click.pass_context
def send_by_template(ctx, template_id, address):
    templ = MailTemplate.objects.get(id=template_id)
    templ.send_to(*address)
