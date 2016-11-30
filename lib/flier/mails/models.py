''' Email Delivery Subsystem
'''
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType


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
    bcc = models.EmailField(
        _('Bcc To'), help_text=_('Bcc To Help'),
        null=True, blank=True, default=None)

    class Meta:
        verbose_name = _('Mail Template')
        verbose_name_plural = _('Mail Template')

    objects = managers.MailTemplateQuerySet.as_manager()


class MailStatus(models.Model, methods.MailStatus):
    '''Mail Status
    '''
    STATUS_DISABLED = 'disabled'
    STATUS_QUEUED = 'queued'
    STATUS_SENDING = 'sending'
    STATUS_SENT = 'sent'
    STATUS = (
        (STATUS_DISABLED, _('Disabled Mail'), ),
        (STATUS_QUEUED, _('Queued Mail'), ),
        (STATUS_SENDING, _('Sending Mail'), ),
        (STATUS_SENT, _('Sent Mail'), ),
    )

    status = models.CharField(
        _('Mail Status'), help_text=_('Mail Status Help'), max_length=20,
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

    recipients = GenericRelation(
        BaseRecipient, related_query_name='mails')

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


class Notification(MailTemplate, methods.Notification):
    content_type = models.OneToOneField(ContentType)
    to = models.EmailField()

    class Meta:
        verbose_name = _('Notification Mail')
        verbose_name_plural = _('Notification Mail')
