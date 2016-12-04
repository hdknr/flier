''' Tasks for smtp
'''
from django.conf import settings
from celery import shared_task
from celery.utils.log import get_task_logger

from email import message_from_file
from email.utils import parseaddr
import traceback
import glob
import os
import time

from flier.models import Recipient
from . import models

logger = get_task_logger('flier')


@shared_task
def save_inbound(transport, sender, recipient, original_recipient,
                 raw_message, process=True, *args, **kwargs):
    '''
    Save `raw_message` (serialized email) to  :ref:`flier.smtp.models.Message`
    This is called by bounce hander defined in SMTP server
    (ex. transport defined in Postfix :ref:`master.cf`).

    1. Create a new `flier.smtp.models.Message`.

    :param string transport: transport name
    :param email sender: sender address
    :param email recipient: recipient address
    :param email original_recipient: origninal recipient address
    :param basestring raw_message: seriazlied email
    '''

    try:
        domain = models.Domain.objects.filter(
            domain=recipient.split('@')[1],
            transport=transport).first()

        message = models.Message.objects.create(
            domain=domain,
            sender=sender,
            recipient=recipient,
            original_recipient=original_recipient,
            raw_message=raw_message, )

        if process:
            message.process_message()

    except:
        logger.error(traceback.format_exc())


@shared_task
def process_drop(*args, **kwargs):
    '''
    process all files under django.conf.settings.FLIER_SMTP_DROP directory
    '''
    drop = getattr(settings, 'FLIER_SMTP_DROP', None)
    if not drop:
        logger.warn('No FLIER_SMTP_DROP defined in settings')
        return 0

    count = 0
    for m in glob.glob(drop + "/*.eml"):
        try:
            res = process_drop_mail(m)
            if res > 0:
                os.remove(m)
            time.sleep(0.1)
            count += 1
        except:
            logger.error(traceback.format_exc())
    return count


@shared_task
def process_drop_mail(path, *args, **kwargs):
    '''
    Process a given mail file.
    Saved to :ref:`flier.smtp.models.Message` and done something

    1. Returned(Bounced back) mail
    2. Forwaring Mail
    3. Bounce back for a forwarded mail
    4. Stray mail
    '''
    if not os.path.isfile(path):
        logger.debug("no such file:", path)
        return -1

    msg = message_from_file(open(path))
    to = msg['Delivered-To'] or msg['To']
    to = to and parseaddr(to)[1]
    logger.debug("processing:{} {}".format(to, path))

    # Bounced Back
    if process_bounced_back(msg, to):
        return 1

    # Forwarding
    if process_forwarding(msg, to):
        return 2

    # Forwarding Bounced
    if process_forwarding_bounced(msg, to):
        return 3

    # Save message just in case
    if process_save(msg, to):
        return 4
    return 5


def process_bounced_back(msg, to):
    if msg and to:
        recipient = Recipient.objects.filter(key=to).first()
        if recipient:
            recipient.bounce(
                status_code='smtp bounce', message=msg.as_string())
            return True
    return False


def process_forwarding(msg, to):
    if msg and to:
        forwarder = models.Forwarder.objects.filter(address=to).first()
        if forwarder:
            forwarder.forward_message(
                models.Message.objects.from_mailobject(
                    msg, status='forwarding'))
            return True
    return False


def process_forwarding_bounced(msg, to):
    if msg and to:
        original = models.Message.objects.filter(relay_from=to).first()
        if original:
            original.bounce_back(
                models.Message.objects.from_mailobject(
                    msg, status='bounced forward'))
            return True
    return False


def process_save(msg, to):
    models.Message.objects.from_mailobject(msg, status='no reason')
    return True
