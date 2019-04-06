from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.dispatch import dispatcher
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


from flier import (methods, managers)


class BaseModel(models.Model, methods.BaseModel):
    '''Base Model
    '''
    created_at = models.DateTimeField(_(u'Created At'), auto_now_add=True, )
    updated_at = models.DateTimeField(_(u'Updated At'), auto_now=True, )

    class Meta:
        abstract = True


class BaseMessage(models.Model):
    bounce_signal = dispatcher.Signal(providing_args=["instance", ])
    delivery_signal = dispatcher.Signal(providing_args=["instance", ])
    complaint_signal = dispatcher.Signal(providing_args=["instance", ])
    confirm_signal = dispatcher.Signal(providing_args=["instance", ])

    class Meta:
        abstract = True


class Sender(BaseModel, methods.Sender):
    name = models.CharField(
        _('Sender Name'), help_text=_('Sender Name Help'),
        max_length=100)
    address = models.EmailField(
        _('Sender Address'), max_length=100)

    wait_every = models.IntegerField(
        _('Wait sending for every count'),
        help_text=_('Wait sending for every count help'),
        default=0)

    wait_ms = models.IntegerField(
        _('Wait milliseconds'),
        help_text=_('Wait milliseconds help'),
        default=0)

    wait_loadaverage = models.FloatField(
        _('Wait Load Average'),
        help_text=_('Wait Load Average Help'),
        default=methods.DEFAULTS['LOADAVERAGE_MAX'])

    enabled = models.BooleanField(_('Enabled Sender'), default=True)

    class Meta:
        verbose_name = _('Sender')
        verbose_name_plural = _('Sender')

    def __unicode__(self):
        return self.address


class Address(BaseModel, methods.Address):
    ''' Mail Address
    '''
    address = models.EmailField(
        _('Email Address'),
        help_text=_('Email Address Help'), max_length=100,
        unique=True, db_index=True)

    domain = models.CharField(
        _('Email Domain'),
        help_text=_('Email Domain Help'), max_length=50,
        null=True, blank=True, default='',)

    bounced = models.IntegerField(
        _('Bounced Count'),
        help_text=_('Bounced Count Help'), default=0)

    enabled = models.BooleanField(
        _('Enabled Address'), help_text=_('Enabled Address Help'),
        default=True)

    class Meta:
        verbose_name = _('Mail Address')
        verbose_name_plural = _('Mail Address')

    def __unicode__(self):
        return u"{}".format(self.address)

    def save(self, *args, **kwargs):
        if self.address:
            self.domain = self.address.split('@')[1]
        super(Address, self).save(*args, **kwargs)


class RecipientStatus(models.Model):
    code = models.CharField(
        _('Recipient Status Code'),
        help_text=_('Recipient Status Code Help'),
        max_length=50, unique=True, db_index=True)

    label = models.CharField(
        _('Recipient Status Label'),
        help_text=_('Recipient Status Label Help'),
        max_length=100, null=True, blank=True, default=None)

    invalid = models.BooleanField(
        _('Invalid Status'), default=False)

    description = models.TextField(
        _('Recipient Status Description'),
        null=True, default=None, blank=True)

    class Meta:
        verbose_name = _('Recipient Status')
        verbose_name_plural = _('Recipient Status')

    objects = managers.RecipientStatusQuerySet.as_manager()

    def __unicode__(self):
        return self.label or self.code


class RecipientContext(models.Model):
    content_type = models.ForeignKey(
        ContentType, verbose_name=_('Recipient Context'),
        null=True, blank=True, default=None)

    object_id = models.PositiveIntegerField(
        _('Recipint Contenxt Instance'),
        null=True, blank=True, default=None)

    content_object = GenericForeignKey('content_type', 'object_id')

    target_content_type = models.ForeignKey(
        ContentType, verbose_name=_('Target Context'),
        related_name='targets',
        null=True, blank=True, default=None)

    target_object_id = models.PositiveIntegerField(
        _('Target Instance'),
        null=True, blank=True, default=None)

    target_object = GenericForeignKey(
        'target_content_type', 'target_object_id')

    class Meta:
        abstract = True


class Recipient(RecipientContext, BaseModel, methods.Recipient):
    '''Recipients for a Mail
    '''
    key = models.CharField(
        _('Recipient Key'), help_text=_('Recipient Key Help'),
        max_length=100, unique=True, db_index=True)

    message_id = models.CharField(
        _('Message ID'), help_text=_('Message ID Help'),
        max_length=100, unique=True, db_index=True)

    sender = models.ForeignKey(
        Sender, verbose_name=_('Message Sender'),
        help_text=_('Message Sender Help'))

    to = models.ForeignKey(
        Address, verbose_name=_('Recipient Address'),
        help_text=_('Recipient Address Help'))

    status = models.ForeignKey(
        RecipientStatus, verbose_name=_('Recipient Status'),
        help_text=_('Recipient Status Help'),
        null=True, default=None, blank=True, on_delete=models.SET_NULL)

    sent_at = models.DateTimeField(
        _('Sent At to Reipient'), help_text=_('Sent At to Recipient Help'),
        null=True, blank=True, default=None)

    message = models.TextField(
        _('Recipient Message'), null=True, default=None, blank=True)

    class Meta:
        verbose_name = _('Recipient')
        verbose_name_plural = _('Recipient')

    objects = managers.RecipientQuerySet.as_manager()

    def __unicode__(self):
        return self.to_id and self.to.__unicode__() or ''

    def save(self, *args, **kwargs):
        if not self.message_id:
            self.message_id = self.sender.create_messageid(
                idstring=self.to_id and str(self.to_id))
        if not self.key:
            self.key = self.message_id
        super(Recipient, self).save(*args, **kwargs)
