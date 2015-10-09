from __future__ import absolute_import
from django.dispatch import receiver
from flier.models import BaseMessage

import logging
logger = logging.getLogger('flier.mails')


@receiver(BaseMessage.confirm_signal)
def confirm(instance, *args, **kwargs):
    # access url # TODO: error logging
    print "confirm"


@receiver(BaseMessage.bounce_signal)
def bounce(instance, *args, **kwargs):
    # TODO: signal bounce
    print "bounce"


@receiver(BaseMessage.delivery_signal)
def delivery(instance, *args, **kwargs):
    # TODO: most of cases, delete notification
    print "delivery"


@receiver(BaseMessage.complaint_signal)
def complaint(instance, *args, **kwargs):
    print 'complaint'
