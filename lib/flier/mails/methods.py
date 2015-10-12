from django.utils.timezone import now, localtime
# from django.utils.encoding import force_text
from django import template
# from django.core.mail import EmailMultiAlternatives

from datetime import timedelta
import time


class Service(object):
    def __init__(self, *args, **kwargs):
        super(Service, self).__init__(*args, **kwargs)
        self._every = 0

    def wait(self):
        self._every = self._every + 1
        if self.wait_every < self._every:
            self._every = 0
            if self.wait_every > 0:
                time.sleep(self.wait_ms / 1000.0)


class MailTemplate(object):

    def render_subject(self, **kwargs):
        return template.Template(self.instance.subject).render(
            template.Context(kwargs))

    def render_body(self, **kwargs):
        return template.Template(self.instance.text).render(
            template.Context(kwargs))

    def create_mail(self, **kwargs):
        return self.mail_set.create(
            subject=self.subject,
            body=self.body,
            html=self.html,
            **kwargs
        )


class BaseMail(object):

    @property
    def subtype(self):
        # TODO: SHOULD BE configurable
        return 'plain'

    def rendered_message(self, mail_address, **kwargs):
        return template.Template(self.body).render(
            template.Context(dict(
                kwargs, to=mail_address,
            )))

    def rendered_html(self, mail_address, **kwargs):
        return template.Template(self.html).render(
            template.Context(dict(
                kwargs, to=mail_address,
            )))

    def create_message(self, recipient, **kwargs):
        '''
        :param Recipient recipient:
        '''
        message = self.sender.instance.create_message(
            subject=self.subject,
            body=self.rendered_message(recipient.to),
            to=[recipient.to.address],            # list of tuple
            headers={'Message-ID': recipient.message_id}, **kwargs)

        if self.html:
            message.attach_alternative(
                self.rendered_html(recipient.to), "text/html")

        return message


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


class Mail(object):
    '''Mail Delivery Definition
    '''

    @property
    def address_model(self):
        pass

    def reset_status(self):
        self.recipient_set.all().update(sent_at=None)
        self.status = self.STATUS_QUEUED
        self.sent_at = None


class Recipient(object):
    '''Recipients for a Mail
    '''

    def create_message(self, **kwargs):
        return self.mail.create_message(self, **kwargs)

    def send_mail(self):
        return self.create_message().send()


class Attachment(object):
    '''Attachemetns for a Mail
    '''
    pass
