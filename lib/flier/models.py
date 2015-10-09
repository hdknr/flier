from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import serializers
from django.contrib.contenttypes.models import ContentType


class BaseModel(models.Model):
    '''Base Model
    '''
    created_at = models.DateTimeField(_(u'Created At'), auto_now_add=True, )
    updated_at = models.DateTimeField(_(u'Updated At'), auto_now=True, )

    class Meta:
        abstract = True

    @classmethod
    def contenttype(cls):
        return ContentType.objects.get_for_model(cls)

    def to_fixture(self):
        return serializers.serialize(
            "json", [self], ensure_ascii=False, indent=4)
