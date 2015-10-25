from django.core import serializers, mail
from django.contrib.contenttypes.models import ContentType

import time


class BaseModel(object):
    '''Base Model
    '''
    @classmethod
    def contenttype(cls):
        return ContentType.objects.get_for_model(cls)

    def to_fixture(self):
        return serializers.serialize(
            "json", [self], ensure_ascii=False, indent=4)


class Sender(object):
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

    def create_messageid(self):
        return mail.make_msgid(domain=self.domain)

    @property
    def instance(self):
        def _cache():
            self._instance = None
            for i in self._meta.related_objects:
                if not issubclass(i.related_model, self._meta.model):
                    continue
                self._instance = i.related_model.objects.filter(
                    **{i.field_name: self.id}).first()
                if self._instance:
                    break
            return self._instance

        return getattr(self, '_instance', _cache())

    def create_recipient(self, address, message_id=None):
        to_filed = self.recipient_set.model._meta.get_field_by_name('to')[0]
        message_id = message_id or self.create_messageid()
        recipient, _ = self.recipient_set.get_or_create(
            key=message_id,             # This key replaced by Sender
            message_id=message_id,
            to=to_filed.related_model.objects.get_or_create(address=address)[0],
        )
        return recipient


class Address(object):
    ''' Mail Address
    '''
    def bounce(self):
        # TODO: send signal for app to disable this address
        self.bounced += 1
        self.save()


class Recipient(object):

    def create_message(self, headers={}, *args, **kwargs):
        headers['Message-ID'] = self.message_id
        return self.sender.instance.create_message(
            to=[self.to.address],
            headers=headers, *args, **kwargs)

    def bounce(self, status, message):
        # TODO send signal to subclass instance
        self.status = status
        self.message = message
        self.save()
        self.to.bounce()
