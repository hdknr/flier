from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.dispatch import dispatcher

import methods


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
        help_text=_('Email Address Help'), max_length=50)

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
        return self.address

    def save(self, *args, **kwargs):
        if self.address and not self.domain:
            self.domain = self.address.split('@')[1]
        super(Address, self).save(*args, **kwargs)


class Log(BaseModel, methods.Log):
    address = models.ForeignKey(Address)
    signal = models.CharField(_('Log Signal'), max_length=50)
    message = models.TextField(_('Log Message'))

    class Meta:
        verbose_name = _('Address Log')
        verbose_name_plural = _('Address Log')
