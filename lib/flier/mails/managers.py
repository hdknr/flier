from django.db import models
from django.utils.timezone import now
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


from furl import furl
from hashlib import md5
from flier.managers import RecipientQuerySet
from . import utils
from logging import getLogger
logger = getLogger('flier')


class MailTemplateQuerySet(models.QuerySet):
    def load_for_name(self, name):
        obj = self.filter(name=name).first()
        if not obj:
            source, path = utils.get_template_source(name)
            text = source or "subject\nbody"
            subject, text = text.split('\n', 1)

            obj = self.objects.create(
                name=name, subject=subject, text=text)

        return obj


class MailQuerySet(models.QuerySet):
    def queueing_set(self, basetime=None):
        basetime = basetime or now()
        return self.filter(
            models.Q(due_at__isnull=True) | models.Q(due_at__lte=basetime), # due_at is passed or not specified # NOQA
            status=self.model.STATUS_QUEUED,    # queued
            sent_at__isnull=True,               # not yet queued
        ).exclude(task_id__regex=r'.+')         # not yet job queued


class MailRecipientQuerySet(RecipientQuerySet):

    def opt(self, mail, address):
        from flier.models import Address
        to, created = Address.objects.get_or_create(address=address)
        return self.get_or_create(mail=mail, to=to, sender=mail.sender)[0]


class MailClickQuerySet(models.QuerySet):

    def generate_url(self, url_name, mail, recipient):
        if not mail.click_url:
            return None

        kwargs = dict(
            message_id=md5(recipient.message_id).hexdigest(),
            mail=mail and mail.id,
            recipient=recipient and recipient.id)
        path = reverse(url_name, kwargs=kwargs)
        return furl(mail.click_url).origin + path

    def click(self, mail, recipient, message_id):
        from flier.mails.models import Mail
        from flier.models import Recipient
        mail = Mail.objects.filter(id=mail).first()
        recipient = Recipient.objects.filter(id=recipient).first()

        if mail and recipient and \
                md5(recipient.message_id).hexdigest() == message_id:
            return self.create(mail=mail, recipient=recipient)

        logger.error(
            _('Invalid Mail Click mail:{} recipient:{} message_id={}').format(
                mail, recipient, message_id))
