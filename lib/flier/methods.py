from django.core import serializers
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


class Address(object):
    ''' Mail Address
    '''
    def bounce(self):
        self.bounced += 1
        self.save()


class Recipient(object):

    def bounce(self, status, message):
        self.status = status
        self.message = message
        self.save()
        self.to.bounce()
