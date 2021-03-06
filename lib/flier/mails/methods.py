from django.utils.timezone import now, localtime
from django import template
from django.contrib.sites.models import Site
from celery.task.control import revoke
from datetime import timedelta
from flier.methods import BaseMethod

from logging import getLogger
logger = getLogger('flier')


class MailTemplate(object):

    def render_subject(self, **kwargs):
        return template.Template(self.instance.subject).render(
            template.Context(kwargs))

    def render_body(self, **kwargs):
        return template.Template(self.instance.body).render(
            template.Context(kwargs))

    def render_html(self, **kwargs):
        if self.instance.html:
            return template.Template(self.instance.html).render(
                template.Context(kwargs))

    def build_message(self, recipient,  **ctx):
        bcc = ctx.get('bcc', tuple(self.bcc and self.bcc.split(',') or []))
        cc = ctx.get('cc', [])
        if 'site' not in ctx:
            try:
                ctx['site'] = Site.objects.get_current()
            except:
                pass
        message = recipient.create_message(
            self.render_subject(to=recipient, mail=self, **ctx),
            self.render_body(to=recipient, mail=self, **ctx),
            bcc=bcc, cc=cc)
        if self.html:
            message.attach_alternative(
                self.render_html(to=recipient, mail=self, **ctx), "text/html")

        return message

    def create_recipient(self, addr, sender=None, instance=None, **kwargs):
        sender = sender or self.sender
        return sender.instance.create_recipient(
            addr, content_object=instance, **kwargs)

    def send_to(self, *address, **ctx):
        sender = ctx.get('sender', None)
        instance = ctx.get('instance', None)
        for addr in address:
            recipient = self.create_recipient(
                addr, sender=sender, instance=instance)
            msg = self.build_message(recipient, **ctx)
            msg.send()


class BaseMail(BaseMethod):

    @property
    def subtype(self):
        # TODO: SHOULD BE configurable
        return 'plain'

    @property
    def text_body(self):
        return self.body

    @property
    def html_body(self):
        return self.html

    def rendered_subject(self, **kwargs):
        return template.Template(self.subject).render(
            template.Context(dict(kwargs, mail=self,)))

    def rendered_message(self, **kwargs):
        return template.Template(self.text_body).render(
            template.Context(dict(kwargs, mail=self,)))

    def rendered_html(self, **kwargs):
        return template.Template(self.html_body).render(
            template.Context(dict(kwargs, mail=self,)))

    def create_message(self, recipient, **kwargs):
        '''
        :param flier.moddels.Recipient recipient:
        '''
        bcc = kwargs.get('bcc', ())
        cc = kwargs.get('cc', ())
        if 'site' not in kwargs:
            try:
                kwargs['site'] = Site.objects.get_current()
            except:
                pass

        message = recipient.create_message(
            subject=self.rendered_subject(recipient=recipient, **kwargs),
            body=self.rendered_message(recipient=recipient, **kwargs),
            cc=cc, bcc=bcc)

        if self.html:
            message.attach_alternative(
                self.rendered_html(recipient=recipient), "text/html")

        return message

    def create_recipient(self, addr, **kwargs):
        return self.sender.instance.create_recipient(
            addr, content_object=self, **kwargs)

    def send_to(self, addr, **kwargs):
        '''Create Recipient, Mesaage and send it. (sync)'''
        self.create_message(
            self.create_recipient(addr, **kwargs), **kwargs).send()

    def active_recipients(self, basetime=None):
        return self.recipients.active_set()

    def all_recipients(self):
        return self.recipients.all()

    def enqueue(self):
        '''Enqueue a Mail to job queue. '''
        from flier.mails import tasks
        r = tasks.send_mail.apply_async(
            [self.id], eta=tasks.make_eta(self.due_at or now()))
        self.task_id = r.id
        self.save()

    def send(self):
        from flier.mails import tasks
        tasks.send_mail(self)


class MailStatus(object):
    '''Mail Status
    '''
    def update_due_at(self, days=0):
        '''Update due_at with `sleep_to` '''
        self.due_at = localtime(now()) + timedelta(days=days)

        # WARN:microsecond is trunctad by MySQL 5.6+
        self.due_at = self.due_at.replace(
            hour=self.sleep_to.hour,
            minute=self.sleep_to.minute,
            second=self.sleep_to.second,
            microsecond=self.sleep_to.microsecond,)
        self.save()

    def delay(self, dt=None):
        '''Mail sending process is delayed until `sleep_to` '''
        dt = dt or localtime(now()).time()

        if any([
            not self.sleep_from, not self.sleep_to, not dt]
        ):
            return False

        if all([
            self.sleep_from <= self.sleep_to,
            self.sleep_from <= dt,
            dt <= self.sleep_to,
        ]):
            # MUST today
            self.update_due_at()
            return True
        if all([
            self.sleep_from > self.sleep_to,
        ]):

            if self.sleep_from <= dt:
                # Tommorrow
                self.update_due_at(1)
                return True

            elif dt <= self.sleep_to:
                # Today
                self.update_due_at()
                return True

        return False

    def is_active(self, dt=None):
        '''Is active mail or not'''
        dt = dt or now()
        return all([
            self.status == self.STATUS_QUEUED,
            self.due_at is None or self.due_at <= dt,
            self.sent_at is None])

    def cancel(self, save=True):
        if self.task_id:
            revoke(self.task_id, terminate=True)
            self.mailcancel_set.get_or_create(task_id=self.task_id)
            self.task_id = ''
            if save:
                self.save()

    def complete(self):
        self.task_id = ''
        self.status = self.STATUS_SENT
        self.sent_at = now()
        self.save()


class Mail(object):
    '''Mail Delivery Definition
    '''

    def reset_status(self):
        self.cancel(save=False)
        self.instance.all_recipients().update(
            sent_at=None, status=None, message='', )
        self.status = self.STATUS_DISABLED
        self.sent_at = None
        self.save()

    def prepare_sending(self):
        ''' prepare for sending. override this method'''
        pass

    def provide(self):
        '''Prepare Recipients and ready to send'''
        self.instance.prepare_sending()     # subclass prepare sending
        self.status = self.STATUS_SENDING
        self.save()                         # post_save signal fires again


class MailCancel(object):

    def cancel(self):
        self.delete()
        self.mail.task_id = ''
        self.mail.save()


class MailRecipient(object):
    '''Recipients for a Mail
    '''
    pass


class Attachment(object):
    '''Attachemetns for a Mail
    '''
    pass


class Notification(object):
    def notify(self, instance, *address, **ctx):
        if 'bcc' not in ctx and self.bcc:
            ctx['bcc'] = self.bcc.split(',')

        ctx['instance'] = instance
        address = address or (self.to, )
        self.send_to(*address, **ctx)  # BaseMail.send_to
