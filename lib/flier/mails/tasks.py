from __future__ import absolute_import
from django.utils.timezone import now, get_current_timezone
from django.dispatch import receiver

from flier.models import Sender, Recipient
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
    return isinstance(instance, model_class) and \
        model_class.objects.get(id=instance.id) or \
        model_class.get(id=instance)


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
def send_mail(sender, mail):
    '''Send mail

    :param Mail mail:  :ref:`emailqueue.models.Mail` or id
    :param list(Email) recipients: List of adhoc recipients.
            If `recipients` is not specified,
    :ref:`emailqueue.models.Recipient` list is used.
    '''
    mail = get_object(mail, models.Mail)
    sender = get_object(sender, Sender)
    sender = sender.instance            # Actual Sender

    if mail.sent_at or mail.status == mail.STATUS_DISABLED:
        # Already completed
        logger.warn(u"{0} {1} {2} {3}".format(
            u"This message has been already processed",
            mail.sent_at, mail.status, mail.subject,
        ))
        return

    # BEGIN:
    if mail.status != mail.STATUS_SENDING:
        mail.status = mail.STATUS_SENDING
        mail.save()         # post_save signle fires again

    # active_set:
    #   - recipients already sent (sent_at is not None)are NOT included
    # TOOD:   mail.get_active_set()
    recipients = mail.recipient_set.active_set()

    for recipient in recipients:

        # INTERUPTED:
        if mail.delay():    # make this Mail pending state
            logger.info("Mail({0}) is delayed".format(mail.id))
            # enqueue another task
            send_mail.apply_async(
                args=[sender.id, mail.id],
                eta=make_eta(mail.due_at))
            # terminate this task
            return

        return_path, to = get_return_path_and_to(mail, recipient)

        if not return_path and not to:
            logger.warn(u"recipient({0}) is not valid".format(recipient))
            continue

        if not to.enabled:
            logger.warn(u"{0} is disabled".format(to.__unicode__()))
            continue

        mail.refresh_from_db()
        if mail.status != mail.STATUS_SENDING:
            logger.warn(u"Sending Mail({0}) has been interrupted".format(
                mail.id))
            return

        msg = sender.create_message(
            from_email=return_path,
            to=[to],
            headers={
                "From": sender.address,
                "To": to,
            })

        msg.send()

        if isinstance(recipient, models.Recipient):
            recipient.sent_at = now()
            recipient.save()

        sender.wait()

    # END: completed sending
    mail.status = mail.STATUS_SENT
    mail.sent_at = now()
    mail.save()


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
