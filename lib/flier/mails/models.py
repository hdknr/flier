''' Email Delivery Subsystem
'''
from django.db import models
from django.utils.translation import ugettext_lazy as _


from flier.models import BaseModel
from flier.mails import (
    methods, managers, fields,
)


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


class Service(BaseModel, methods.Service):
    name = models.CharField(
        _('Mail Service Name'), unique=True, max_length=50)

    domain = models.CharField(
        _('Mail Domain Name'), unique=True, max_length=50)

    wait_every = models.IntegerField(
        _('Wait sending for every count'),
        help_text=_('Wait sending for every count help'),
        default=0)

    wait_ms = models.IntegerField(
        _('Wait milliseconds'),
        help_text=_('Wait milliseconds help'),
        default=0)

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Service')

    def __unicode__(self):
        return self.name


class BaseMail(BaseModel, methods.BaseMail):
    sender = models.EmailField(
        _('Mail Sender'), help_text=_('Mail Sender Help'), max_length=50)

    subject = models.TextField(
        _('Mail Subject'), help_text=_('Mail Subject Help'), )

    body = models.TextField(
        _('Mail Body'), help_text=_('Mail Body Help'), )

    html = models.TextField(
        _('Mail HTML Body'), help_text=_('Mail HTML Body Help'),
        null=True, blank=True, default=None)

    class Meta:
        abstract = True


class MailTemplate(BaseMail, methods.MailTemplate):
    name = models.CharField(
        _('Mail Name'), help_text=_('Mail Name Help'),  max_length=200,
        unique=True, db_index=True)

    class Meta:
        verbose_name = _('Mail Template')
        verbose_name_plural = _('Mail Template')

    objects = managers.MailTemplateQuerySet.as_manager()


class MailStatus(models.Model, methods.MailStatus):
    '''Mail Status
    '''
    STATUS_DISABLED = 0
    STATUS_QUEUED = 10
    STATUS_SENDING = 20
    STATUS_SENT = 30
    STATUS = (
        (STATUS_DISABLED, _('Disabled Mail'), ),
        (STATUS_QUEUED, _('Queued Mail'), ),
        (STATUS_SENDING, _('Sending Mail'), ),
        (STATUS_SENT, _('Sent Mail'), ),
    )

    status = models.IntegerField(
        _('Mail Status'), help_text=_('Mail Status Help'),
        default=STATUS_DISABLED, choices=STATUS)

    due_at = models.DateTimeField(
        _('Due At'), help_text=_('Due At'),
        null=True, blank=True, default=None)

    sent_at = models.DateTimeField(
        _('Sent At'), help_text=_('Sent At Help'),
        null=True, blank=True, default=None)

    sleep_from = models.TimeField(
        _('Sleep From'), help_text=_('Sleep From Help'),
        null=True, blank=True, default=None)

    sleep_to = models.TimeField(
        _('Sleep To'), help_text=_('Sleep To Help'),
        null=True, blank=True, default=None)

    class Meta:
        abstract = True


class Mail(BaseMail, MailStatus, methods.Mail):
    '''Mail Delivery Definition
    '''
    template = models.ForeignKey(
        MailTemplate, null=True, default=None, blank=True,
        on_delete=models.SET_NULL)

    ctx = models.TextField(
        _('Context Data'), help_text=_('Context Data Help'),
        default=None, null=True, blank=True)

    class Meta:
        verbose_name = _('Mail')
        verbose_name_plural = _('Mail')

    objects = managers.MailQuerySet.as_manager()

    def __unicode__(self):
        return self.subject


class Recipient(BaseModel, methods.Recipient):
    '''Recipients for a Mail
    '''
    mail = models.ForeignKey(
        Mail, verbose_name=_('Mail'), help_text=_('Mail Help'))

    to = models.ForeignKey(
        Address, verbose_name=_('Recipient Address'),
        help_text=_('Recipient Address Help'))

    return_path = models.EmailField(
        _('Return Path'), help_text=_('Return Path Help'), max_length=50,
        null=True, default=None, blank=True)

    sent_at = models.DateTimeField(
        _('Sent At to Reipient'), help_text=_('Sent At to Recipient Help'),
        null=True, blank=True, default=None)

    class Meta:
        verbose_name = _('Recipient')
        verbose_name_plural = _('Recipient')

    objects = managers.RecipientQuerySet.as_manager()

    def __unicode__(self):
        return self.to.__unicode__()


class Attachment(BaseModel, methods.Attachment):
    '''Attachemetns for a Mail
    '''
    mail = models.ForeignKey(
        Mail, verbose_name=_('Mail'), help_text=_('Mail Help'))

    file = fields.FileField(
        _('Attachment File'),
        help_text=_('Attrachment File Help'),)

    class Meta:
        verbose_name = _('Attachment')
        verbose_name_plural = _('Attachment')
