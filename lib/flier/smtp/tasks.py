''' Tasks for smtp
'''

from celery import shared_task
from celery.utils.log import get_task_logger

import traceback
import models

logger = get_task_logger(__name__)


@shared_task
def save_inbound(transport, sender, recipient, original_recipient,
                 raw_message, *args, **kwargs):
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

        message.process_message()

    except:
        logger.error(traceback.format_exc())
