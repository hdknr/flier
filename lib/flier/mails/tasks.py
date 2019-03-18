# coding: utf-8
from __future__ import absolute_import
from django.utils.timezone import now, get_current_timezone
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from flier.models import Recipient, RecipientStatus
from flier.mails import (models, utils)
from flier.backends import BackendSignal

from celery import shared_task
# from celery.utils.log import get_task_logger

import traceback
from logging import getLogger

logger = getLogger('flier')


def make_eta(when=None):
    '''ETA(estimated time of arrival) time

        :param when:  :py:class:`datetime.datetime`
        :return: :py:class:`datetime.datetime` with timezone
    '''
    when = when or now()
    return when.tzinfo and when or get_current_timezone().localize(when)


def get_object(instance, model_class):
    mail = isinstance(instance, model_class) and \
        model_class.objects.get(id=instance.id) or \
        model_class.objects.get(id=instance)
    # return mail.instance        # return subclass instance if exists
    return mail


def get_return_path_and_to(sender, mail, recipient):

    if isinstance(recipient, basestring):
        to = models.Address.objects.get_or_create(
            address=recipient)[0]
        return_path = utils.to_return_path(
            'adhoc', sender.id, mail.id, to.id)

    elif isinstance(recipient, models.Recipient) and \
            recipient.mail == mail:
        to = recipient.to
        return_path = recipient.return_path

    return (return_path, to, )


@shared_task
def enqueue_mails():
    '''Enqueue mails '''
    mails = models.Mail.objects.queueing_set()
    for mail in mails:
        mail.enqueue()
        logger.info(u'{0} has been enqueued task_id={1}'.format(
            mail.id, mail.task_id))

    logger.info(
        u'enqueue_mails:{0} mails has been enqueued .'.format(mails.count()))


@shared_task
def send_mail(mail, withbreak=True):
    '''Send mail

    :param Mail mail:  :ref:`emailqueue.models.Mail` or id
    '''
    mail = get_object(mail, models.Mail)
    job = getattr(send_mail, 'request', None)

    if job:
        for cancel in mail.instance.mailcancel_set.filter(
                task_id=send_mail.request.id):
            cancel.cancel()
            logger.warn(u'{0} has been canceled'.format(job.id))
            return

    if mail.status == mail.STATUS_DISABLED:
        # Already completed
        logger.warn(u"{} sent_at:{} status:{} subject:{}".format(
            _("send_mail:This mail is not in sending queue."),
            mail.sent_at, mail.get_status_display(), mail.subject))
        return

    if mail.sent_at:
        # Already completed
        logger.warn(u"{0} sent_at:{1} status:{2} subject:{3}".format(
            _("send_mail:This message has been already processed"),
            mail.sent_at, mail.get_status_display(), mail.subject,))
        return

    # BEGIN:
    if mail.status == mail.STATUS_QUEUED:
        mail.provide()()

    sender = mail.sender.instance               # Actual Sender
    recipients = mail.active_recipients()       # Mail Recipient list
    logger.warn(_("send_mail:Sending sender:{} recipeints:{}").format(
        sender.address, recipients.count()))

    for recipient in recipients:

        # INTERUPTED:
        if withbreak and mail.delay():    # make this Mail pending state
            logger.info(_("send_mail:Mail({0}) is delayed").format(mail.id))
            # enqueue the other task for sending this Mail
            if job:
                mail.enqueue()
            # terminate this task
            return

        # Get latest Mail.status
        mail.refresh_from_db()
        if mail.status != mail.STATUS_SENDING:
            logger.warn(
                _("send_mail:Mail<{}> has been interrupted status:{}").format(
                    mail.id, mail.get_status_display()))
            return

        # Send mail to each recipient
        msg = mail.instance.create_message(recipient)
        msg.send()

        # Wait
        sender.wait()

    # END: completed sending
    logger.warn(
        _("send_mail: completed for Mail({})").format(mail.id,))
    mail.complete()


@receiver(BackendSignal.sent_signal)
def on_sent(sender=None, from_email=None, to=None, message_id=None, key=None,
            status_code='sent', message='', **kwargs):

    recipient = Recipient.objects.filter(message_id=message_id).first()
    if not recipient:
        logger.error(u"Recpient for message-id({}) does not exists".format(
            message_id))
        return

    try:
        recipient.key = key
        recipient.sent_at = now()
        recipient.status = RecipientStatus.objects.get_status(status_code)
        recipient.message = message
        recipient.save()
    except:
        status_code = 'post send error'
        recipient.status = RecipientStatus.objects.get_status(status_code)
        recipient.sent_at = now()
        recipient.message = message + "\n" + traceback.format_exc()
        recipient.save()


@receiver(BackendSignal.failed_signal)
def on_failed(sender=None, from_email=None, to=None, message_id=None, key=None,
              status_code='sent', message='', **kwargs):
    Recipient.objects.filter(message_id=message_id).update(
        key=key,
        sent_at=now(),
        status=RecipientStatus.objects.get_status(status_code),
        message=message)
