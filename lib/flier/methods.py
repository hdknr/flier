from django.contrib.contenttypes.models import ContentType
from django.core import serializers, mail
from django.core.exceptions import ValidationError
from django.db.models.fields.related import OneToOneRel

from email.header import Header
from email.utils import formataddr
from .validators import validate_email
import os
from . import utils
import time
from logging import getLogger
logger = getLogger('flier')


DEFAULTS = dict(
    LOADAVERAGE_MAX=1.0,
    LOADAVERAGE_WAIT=1000.0,
)


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
                if all([
                    isinstance(i, OneToOneRel),
                    issubclass(i.related_model, self._meta.model)
                ]):
                    self._instance = i.related_model.objects.filter(
                        **{i.field_name: self.id}).first()
                    if self._instance:
                        break
            self._instance = self._instance or self
            return self._instance

        return getattr(self, '_instance', _cache())


class Sender(BaseMethod):

    def __init__(self, *args, **kwargs):
        super(Sender, self).__init__(*args, **kwargs)
        self._every = 0

    def sleep(self, ms=None):
        ms = ms or self.wait_ms / 1000.0
        time.sleep(ms)
        self.refresh_from_db()      # re-read settings

    def wait(self):
        self._every = self._every + 1

        la1, la5, la15 = os.getloadavg()
        if la1 >= self.wait_loadaverage:
            self._every = 0
            logger.warn(
                'Sender{}: wait {}msec: Load {} > {}'.format(
                    self.id, self.wait_ms, self.wait_loadaverage, la1))
            self.sleep()

        elif self.wait_every < self._every:
            self._every = 0
            if self.wait_every > 0:
                logger.warn(
                    'Sender{}: waits for each {} sending: {}msec'.format(
                        self.id, self.wait_every, self.wait_ms))
                self.sleep()

    @property
    def domain(self):
        return self.address.split('@')[1]

    def create_messageid(self, idstring=None):
        idstring = idstring or utils.get_random_string(8)
        return mail.make_msgid(idstring=idstring, domain=self.domain)

    def create_recipient(
            self, address, message_id=None, content_object=None):
        to_field = self.recipient_set.model._meta.get_field('to')
        to, _ = to_field.related_model.objects.get_or_create(address=address)
        message_id = message_id or self.create_messageid(
            idstring=unicode(to.id))

        content_type, object_id = None, None
        if content_object:
            try:
                content_type = ContentType.objects.get_for_model(content_object)
                object_id = content_object.id
            except:
                pass

        recipient, _ = self.recipient_set.get_or_create(
            key=message_id,             # This key replaced by Sender
            message_id=message_id,
            to=to,
            content_type=content_type, object_id=object_id,)

        return recipient

    def to_addr(self):
        h = Header(self.name, 'utf8')
        h = str(h).replace('?=\n ', '')  # newline
        return formataddr((h, self.address))


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

    def bounce(self, status_code, message):
        from .models import RecipientStatus
        self.status = RecipientStatus.objects.get_status(status_code)
        self.message = message
        self.save()
        self.to.bounce()
