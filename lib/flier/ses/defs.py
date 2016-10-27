from django.db import models
from django.utils.translation import ugettext_lazy as _

from flier.models import BaseModel


class Topic(BaseModel):
    BOUNCE = 0
    COMPLAINT = 1
    DELIVERY = 2

    NOTIFICATION_TYPES = ['Bounce', 'Complaint', 'Delivery']

    topic = models.IntegerField(
        _('Topic'), choices=(
            (BOUNCE, _('Bounce Topic')),
            (COMPLAINT, _('Complaint Topic')),
            (DELIVERY, _('Delivery Topic')),), default=BOUNCE)

    arn = models.CharField(
        _('Topic Arn'),
        help_text=_('Topic Arn Help'),
        max_length=100, null=True, default=None, blank=True)

    class Meta:
        abstract = True
