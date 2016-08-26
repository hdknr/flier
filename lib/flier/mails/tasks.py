from __future__ import absolute_import
from django.utils.timezone import now, get_current_timezone
from django.dispatch import receiver

from flier.models import Recipient
from flier.mails import (models, utils)
from flier.backends import BackendSignal

from celery import shared_task
# from celery.utils.log import get_task_logger

import logging

logger = logging.getLogger('flier.mails')
# logger = get_task_logger('flier.mails')
# import traceback


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
    for mail in models.Mail.objects.queueing_set():
        mail.enqueue()
        logger.info(u'{0} has been enqueued task_id={1}'.format(
            mail.id, mail.task_id))


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
        logger.warn(u"{0} sent_at:{1} status:{2} subject:{3}".format(
            u"This mail is not in sending queue.",
            mail.sent_at, mail.get_status_display(), mail.subject,
        ))
        return

    if mail.sent_at:
        # Already completed
        logger.warn(u"{0} sent_at:{1} status:{2} subject:{3}".format(
            u"This message has been already processed",
            mail.sent_at, mail.get_status_display(), mail.subject,
        ))
        return

    # BEGIN:
    if mail.status == mail.STATUS_QUEUED:
        mail.prepare_sending()
        mail.status = mail.STATUS_SENDING
        mail.save()         # post_save signal fires again

    sender = mail.sender.instance            # Actual Sender
    recipients = mail.active_recipients()    # Recipient list
    logger.debug(u"sender:{} recipeints:{}".format(
        sender.address, recipients.count()))

    for recipient in recipients:

        # INTERUPTED:
        if withbreak and mail.delay():    # make this Mail pending state
            logger.info("Mail({0}) is delayed".format(mail.id))

            # enqueue the other task for sending this Mail
            if job:
                send_mail.apply_async(
                    args=[mail.id], eta=make_eta(mail.due_at))

            # terminate this task
            return

        # Get latest Mail.status
        mail.refresh_from_db()
        if mail.status != mail.STATUS_SENDING:
            logger.warn(u"Sending Mail({0}) has been interrupted".format(
                mail.id))
            return

        # Send mail to each recipient
        msg = mail.create_message(recipient)
        msg.send()

        # Wait
        sender.wait()

    # END: completed sending
    mail.complete()


@receiver(BackendSignal.sent_signal)
def on_sent(sender=None, from_email=None, to=None, message_id=None, key=None,
            status='sent', message='', **kwargs):

    Recipient.objects.filter(message_id=message_id).update(
        key=key,
        sent_at=now(),
        status=status,
        message=message)


@receiver(BackendSignal.failed_signal)
def on_failed(sender=None, from_email=None, to=None, message_id=None, key=None,
              status='sent', message='', **kwargs):
    Recipient.objects.filter(message_id=message_id).update(
        key=key,
        sent_at=now(),
        status=status,
        message=message)
