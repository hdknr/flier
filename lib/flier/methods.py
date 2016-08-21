from django.core import serializers, mail
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from email.header import Header
from email.utils import formataddr
import time

import utils


class BaseModel(object):
    '''Base Model
    '''
    @classmethod
    def contenttype(cls):
        return ContentType.objects.get_for_model(cls)

    def to_fixture(self):
        return serializers.serialize(
            "json", [self], ensure_ascii=False, indent=4)


class BaseMethod(object):

    @property
    def instance(self):
        def _cache():
            self._instance = self
            for i in self._meta.related_objects:
                if not issubclass(i.related_model, self._meta.model):
                    continue
                self._instance = i.related_model.objects.filter(
                    **{i.field_name: self.id}).first()
                if self._instance:
                    break
            return self._instance

        return getattr(self, '_instance', _cache())


class Sender(BaseMethod):
    def __init__(self, *args, **kwargs):
        super(Sender, self).__init__(*args, **kwargs)
        self._every = 0

    def wait(self):
        self._every = self._every + 1
        if self.wait_every < self._every:
            self._every = 0
            if self.wait_every > 0:
                time.sleep(self.wait_ms / 1000.0)

    @property
    def domain(self):
        return self.address.split('@')[1]

    def create_messageid(self, idstring=None):
        idstring = idstring or utils.get_random_string(8)
        return mail.make_msgid(idstring=idstring, domain=self.domain)

    def create_recipient(self, address, message_id=None):
        to_field = self.recipient_set.model._meta.get_field('to')
        to, _ = to_field.related_model.objects.get_or_create(address=address)
        message_id = message_id or self.create_messageid(
            idstring=unicode(to.id))
        recipient, _ = self.recipient_set.get_or_create(
            key=message_id,             # This key replaced by Sender
            message_id=message_id,
            to=to,
        )
        return recipient

    def to_addr(self):
        h = Header(self.name, 'utf8')
        return formataddr((str(h), self.address))


class Address(object):
    ''' Mail Address
    '''
    def bounce(self):
        # TODO: send signal for app to disable this address
        self.bounced += 1
        self.save()

    @classmethod
    def get_on_valid(cls, address):
        try:
            validate_email(address)
            return cls.objects.get_or_create(address=address)[0]
        except ValidationError:
            return None


class Recipient(object):

    def create_message(
            self,
            subject='', body='',
            bcc=None, attachments=None, headers={},
            cc=None, reply_to=None, *args, **kwargs):

        '''Create  :ref:`django.core.mail.message.EmailMessage` derived
        class instance
        '''
        headers['Message-ID'] = self.message_id
        headers['From'] = self.sender.to_addr()
        return self.sender.instance.create_message(
            to=[self.to.address],
            subject=subject, body=body,
            bcc=bcc, attachments=attachments, headers=headers,
            cc=cc, reply_to=reply_to, *args, **kwargs)

    def bounce(self, status, message):
        # TODO send signal to subclass instance
        self.status = status
        self.message = message
        self.save()
        self.to.bounce()
