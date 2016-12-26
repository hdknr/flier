# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from flier.mails.models import MailClick
import traceback
from logging import getLogger

logger = getLogger('flier')
register = template.Library()


@register.simple_tag(takes_context=True)
def click_url(context, url_name=None):
    ''' filers.mails.methods.BaseMail.create_message '''
    try:
        url_name = url_name or getattr(
            settings, 'FLIER_MAILS_CLICK', 'fliermails_click')
        mail = context.get('mail', None)
        recipient = context.get('recipient', None)
        return MailClick.objects.generate_url(url_name, mail, recipient)
    except:
        logger.error(traceback.format_exc())
