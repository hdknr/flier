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
        max_length=30)
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


class RecipientContext(models.Model):
    content_type = models.ForeignKey(
        ContentType, verbose_name=_('Recipient Context'),
        null=True, blank=True,)

    object_id = models.PositiveIntegerField(
        _('Recipint Contenxt Instance'),
        null=True, blank=True)

    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True


class Recipient(RecipientContext, BaseModel, methods.Recipient):
    '''Recipients for a Mail
    '''
    key = models.CharField(
        _('Recipient Key'), help_text=_('Recipient Key'),
        max_length=100, unique=True, db_index=True)

    sender = models.ForeignKey(
        Sender, verbose_name=_('Message Sender'),
        help_text=_('Message Sender Help'))

    to = models.ForeignKey(
        Address, verbose_name=_('Recipient Address'),
        help_text=_('Recipient Address Help'))

    message_id = models.CharField(
        _('Message ID'), max_length=100, null=True, db_index=True)

    sent_at = models.DateTimeField(
        _('Sent At to Reipient'), help_text=_('Sent At to Recipient Help'),
        null=True, blank=True, default=None)

    status = models.CharField(_('Recipient Status'), max_length=50)
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
