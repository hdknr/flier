from __future__ import absolute_import
from django.dispatch import receiver

from flier.models import BaseMessage, Recipient, Address, RecipientStatus
from flier.ses import models
# from celery.utils.log import get_task_logger

from logging import getLogger

logger = getLogger('flier.ses')


@receiver(BaseMessage.confirm_signal, sender=models.Notification)
def confirm(instance, *args, **kwargs):
    # TODO: error logging
    instance.confirm()


@receiver(BaseMessage.bounce_signal, sender=models.Notification)
def bounce(instance, *args, **kwargs):
    # TODO: signal bounce
    logger.debug('bounce')

    msg = instance.message_object.Message
    sender = models.Sender.objects.filter(address=msg.mail.source).first()

    for r in msg.bounce.bouncedRecipients:
        to, _ = Address.objects.get_or_create(address=r.emailAddress)
        recipient, _ = Recipient.objects.get_or_create(
            sender=sender, key=msg.mail.messageId, to=to)
        status_code = "{0} {1}".format(r.action, r.status)
        recipient.status = RecipientStatus.objects.get_status(status_code)
        recipient.message = msg.format()
        recipient.save()
        to.bounce()


@receiver(BaseMessage.complaint_signal, sender=models.Notification)
def complaint(instance, *args, **kwargs):
    logger.debug('complaint')

    msg = instance.message_object.Message
    sender = models.Sender.objects.filter(address=msg.mail.source).first()

    for r in msg.complaint.complainedRecipients:
        to, _ = Address.objects.get_or_create(address=r.emailAddress)
        recipient, _ = Recipient.objects.get_or_create(
            sender=sender, key=msg.mail.messageId, to=to)
        status_code = "complaint {0}".format(
            msg.complaint.complaintFeedbackType)
        recipient.status = RecipientStatus.objects.get_status(status_code)
        recipient.message = msg.format()
        recipient.save()
        to.bounce()


@receiver(BaseMessage.delivery_signal, sender=models.Notification)
def delivery(instance, *args, **kwargs):
    # TODO: most of cases, do NOTHING and delete notification
    logger.debug('delivery')
    # create_log('delivery', instance)
