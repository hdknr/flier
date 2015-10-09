from __future__ import absolute_import
from django.dispatch import receiver
import models

import logging
logger = logging.getLogger('flier.mails')


@receiver(models.BaseMessage.confirm_signal, sender=models.BaseMessage)
def confirm(instance, *args, **kwargs):
    # access url # TODO: error logging
    pass


@receiver(models.BaseMessage.bounce_signal, sender=models.BaseMessage)
def bounce(instance, *args, **kwargs):
    # TODO: signal bounce
    pass


@receiver(models.BaseMessage.delivery_signal, sender=models.BaseMessage)
def delivery(instance, *args, **kwargs):
    # TODO: most of cases, delete notification
    pass


@receiver(models.BaseMessage.complaint_signal, sender=models.BaseMessage)
def complaint(instance, *args, **kwargs):
    pass
