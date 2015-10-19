from django.db import models
from django.utils.translation import ugettext_lazy as _

from flier.models import (
    BaseModel, Sender as BaseSender, Address)
import methods
import managers


class Domain(BaseModel, methods.Domain):
    '''Domain:

    - used for :ref:`postfix.relay_domains`, :ref:`postfix.transport_maps`
    '''
    domain = models.CharField(
        _('Domain'), max_length=50, unique=True, db_index=True,)
    '''`where_field`, also `select_field` for relay_domains '''

    transport = models.CharField(
        _('Transport'), max_length=200)
    '''`where_field` for transport_maps'''

    alias_domain = models.ForeignKey(
        'Domain', verbose_name=_('Alias Transport'),
        related_name='alias_domain_set',
        null=True, default=None, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Domain')
        verbose_name_plural = _('Domain')

    objects = managers.DomainQuerySet.as_manager()

    def __unicode__(self):
        return self.domain


class Alias(BaseModel, methods.Domain):
    '''Alias

    - Used in :ref:`postfix.virtual_alias_maps`
    '''
    domain = models.ForeignKey(
        Domain,
        null=True, default=None, blank=True, on_delete=models.SET_NULL)

    recipient = models.EmailField(
        _('Recipient Address'), max_length=100, unique=True, db_index=True)
    '''`where_field` for virtual_alias_maps '''

    forward = models.EmailField(
        _('Forward Address'), max_length=100)
    '''`select_field` for virtual_alias_maps '''

    class Meta:
        verbose_name = _('Alias')
        verbose_name_plural = _('Alias')

    def __unicode__(self):
        return u"{0}>{1}".format(self.recipient, self.forward)


class Sender(BaseSender, methods.Sender):
    domain = models.ForeignKey(
        Domain, verbose_name=_('Sender Domain'), max_length=50)

    class Meta:
        verbose_name = _('Sender')
        verbose_name_plural = _('Sender')

    def __unicode__(self):
        return u"smtp:{0}".format(self.address)


class Forwarder(BaseModel, methods.Forwarder):
    ''' Mail Forwarding Definition
    '''
    domain = models.ForeignKey(
        Domain, verbose_name=_('Sending Domain'),)

    address = models.EmailField(
        _('Forwarder Address'), help_text=_('Forwarder Address Help'),
        max_length=50)

    forward = models.ForeignKey(
        Address, verbose_name=_('Forward Address'),
        help_text=_('Forward Address Help'),
        null=True, blank=True, default=None, on_delete=models.SET_DEFAULT)

    deleted = models.BooleanField(
        _('Is Deleted'), help_text=_('Is Deleted Help'), default=False, )

    task = models.TextField(
        _('Forwarder Task'), help_text=_('Forwarder Task Help'),
        null=True, blank=True, default=None)

    blacklist = models.TextField(
        _('Black List Pattern'),
        help_text=_('Black List Pattern Help'),
        null=True, blank=True, default=None)

    class Meta:
        verbose_name = _('Forwarder')
        verbose_name_plural = _('Forwarder')

    objects = managers.ForwarderQuerySet.as_manager()

    def __unicode__(self):
        to = self.forward and self.forward.address or ''
        return u"{0} >> {1}".format(self.address, to,)


class Relay(BaseModel, methods.Relay):
    ''' Relay Entries for Forwarder
    '''
    forwarder = models.ForeignKey(
        Forwarder,
        verbose_name=_('Original Recipient Forwarder'),
        help_text=_('Original Recipient Forwarder Help'))

    sender = models.ForeignKey(
        Address,
        verbose_name=_('Original Sender Address'),
        help_text=_('Original Sender Address Help'))

    is_spammer = models.BooleanField(
        _('Is Spammer'), default=False)
    '''`Forwarder` owner can check this `sender` is a spammer.'''

    class Meta:
        verbose_name = _('Relay')
        verbose_name_plural = _('Relay')

    objects = managers.RelayQuerySet.as_manager()

    def __unicode__(self):
        return u"{0} > {1}".format(
            self.sender.__unicode__(),
            self.forwarder.__unicode__(),)


class MailMessage(models.Model, methods.MailMessage):
    raw_message = models.TextField(
        _(u'Raw Message Text'), help_text=_(u'Raw Message Text Help'),
        default=None, blank=True, null=True)

    class Meta:
        abstract = True


class RelayedMessage(models.Model, methods.RelayedMessage):
    relay = models.ForeignKey(
        Relay, verbose_name=_('Forwarding Relay'),
        default=None, blank=True, null=True)

    relay_from = models.EmailField(
        _('Relay From'), max_length=50,
        default=None, blank=True, null=True, db_index=True)

    class Meta:
        abstract = True


class Message(MailMessage, RelayedMessage, methods.Message):
    ''' Raw Message '''
    domain = models.ForeignKey(
        Domain, verbose_name=_('Recipient Domain'),
        default=None, blank=True, null=True)

    sender = models.EmailField(
        _('Sender'), help_text=_('Sender Help'),  max_length=100,
        default=None, blank=True, null=True)

    recipient = models.EmailField(
        _('Recipient'), help_text=_('Recipient Help'), max_length=100,
        default=None, blank=True, null=True)

    original_recipient = models.EmailField(
        _('Original Recipient'),
        help_text=_('Oringinal Recipient Help'), max_length=100,
        default=None, blank=True, null=True)

    processed_at = models.DateTimeField(
        _('Processed At'), null=True, blank=True, default=None)

    class Meta:
        verbose_name = _(u'Message')
        verbose_name_plural = _(u'Message')

    objects = managers.MessageQuerySet.as_manager()

    @property
    def forwarder_model(self):
        return Forwarder
