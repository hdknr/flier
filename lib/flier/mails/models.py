''' Email Delivery Subsystem
'''
from django.db import models
from django.utils.translation import ugettext_lazy as _


from flier.models import (
    BaseModel, Sender, Recipient as BaseRecipient)
from flier.mails import (
    methods, managers, fields,
)


class BaseMail(BaseModel, methods.BaseMail):
    sender = models.ForeignKey(
        Sender, verbose_name=_('Mail Sender'), help_text=_('Mail Sender Help'))

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

    task_id = models.CharField(
        _('Task ID'), help_text=_('Task ID Help'),  max_length=40,
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


class MailCancel(BaseModel, methods.MailCancel):
    mail = models.ForeignKey(Mail)
    task_id = models.CharField(
        _('Task ID'), help_text=_('Task ID Help'),  max_length=40,
        db_index=True, unique=True,)

    class Meta:
        verbose_name = _('Mail Cancel')
        verbose_name_plural = _('Mail Cancel')


class MailRecipient(BaseRecipient, methods.MailRecipient):
    mail = models.ForeignKey(Mail)

    class Meta:
        verbose_name = _('Mail Recipient')
        verbose_name_plural = _('Mail Recipient')

    objects = managers.MailRecipientQuerySet.as_manager()

    def save(self, *args, **kwargs):
        super(MailRecipient, self).save(*args, **kwargs)


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
