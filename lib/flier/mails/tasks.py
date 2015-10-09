from __future__ import absolute_import
from django.dispatch import receiver
from flier.models import BaseMessage
from flier.mails.models import Address


import logging
logger = logging.getLogger('flier.mails')


def create_log(signal, instance):
    for a in instance.get_address_list():
        a, created = Address.objects.get_or_create(address=a)
        a.log_set.create(signal=signal, message=instance.get_message(),)
        a.bounce()


@receiver(BaseMessage.confirm_signal)
def confirm(instance, *args, **kwargs):
    # TODO: error logging
    instance.confirm()


@receiver(BaseMessage.bounce_signal)
def bounce(instance, *args, **kwargs):
    # TODO: signal bounce
    logger.debug('bounce')
    create_log('bounce', instance)


@receiver(BaseMessage.delivery_signal)
def delivery(instance, *args, **kwargs):
    # TODO: most of cases, do NOTHING and delete notification
    logger.debug('delivery')
    # create_log('delivery', instance)


@receiver(BaseMessage.complaint_signal)
def complaint(instance, *args, **kwargs):
    logger.debug('complaint')
    create_log('complaint', instance)
