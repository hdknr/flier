from django.core.mail.message import EmailMultiAlternatives
from django.utils.encoding import smart_str

from email import message_from_string
import backends
import uuid
from flier.models import Recipient, Address


class Domain(object):
    '''Domain:
    '''
    def __unicode__(self):
        return self.domain

    def create_alias_domain(self, name):
        domain, created = self.objects.get_or_create(
            doamin=name, transport='error',
            alias=self)
        return domain

    def add_alias_address(self, user, alias_user=None):
        if not self.alias_domain:
            return
        src = '{0}@{1}'.format(user, self.domain)
        dst = '{0}@{1}'.format(alias_user or user, self.alias_domain.domain)
        alias = self.alias_set.filter(recipient=src).first()
        if alias:
            alias.forward = dst
            alias.save()
        else:
            alias = self.alias_set.create(recipient=src, forward=dst)
        return alias

    def verp(self):
        # TODO: better address
        return uuid.uuid1().hex + "@" + self.domain


class Alias(object):
    pass


class Sender(object):
    def verp(self):
        return uuid.uuid1().hex + "." + self.address

    @property
    def backend(self):
        return backends.SmtpBackend()

    @property
    def instance(self):
        return self

    def create_message(self, *args, **kwargs):
        kwargs['from_email'] = self.verp()
        headers = kwargs.get('headers', {})
        headers['From'] = self.address
        kwargs['headers'] = headers
        EmailMultiAlternatives.encoding = kwargs.get('encoding',  None)
        return EmailMultiAlternatives(
            connection=self.backend,
            *args, **kwargs)


class Forwarder(object):
    def forward_message(self, message):
        sender, _ = Address.objects.get_or_create(address=message.sender)
        message.relay, _ = self.relay_set.get_or_create(sender=sender)
        message.relay_from = self.domain.verp()
        message.save()

        backends.SmtpBackend().send_raw_message(
            message.relay_from, self.forward.address,
            message.raw_message)


class Relay(object):
    pass


class MailMessage(object):

    def load_message(self, path):
        '''Load Raw Message '''
        self._mailobject = None     # clear cache
        with open(path) as src:
            self.raw_message = src.read()

    @property
    def mailobject(self):
        ''' return mail object

        :rtype: email.message.Message
        '''
        def _cached():
            # cache message_from_string(self.raw_message)
            self._mailobject = message_from_string(
                smart_str(self.raw_message))

            # self.raw_message.encode('utf8'))
            return self._mailobject

        return getattr(self, '_mailobject', _cached())

    @property
    def is_multipart(self):
        return self.mailobject and self.mailobject.is_multipart() or False

    @property
    def dsn(self):
        ''' DSN object if a Message has something wrong. '''
        def _cached():
            if self.is_multipart and isinstance(
                    self.mailobject.get_payload(), list):
                # cache dns
                self._dsn = self.mailobject.get_payload(1)
                return self._dsn
            return None

        return getattr(self, '_dsn', _cached())

    @property
    def dsn_action(self):
        try:
            return self.dsn and self.dsn.get_payload(1)['action']
        except:
            return None

    @property
    def dsn_status(self):
        try:
            return self.dsn and self.dsn.get_payload(1)['status']
        except:
            return None

    def save_to_file(self, path):
        with open(path, 'w') as out:
            out.write(self.mailobject.as_string())


class RelayedMessage(object):
    @property
    def relay_return_path(self):
        '''Return-Path for Relay

        - used for forwarding Message
        '''
        return self.relay and self.relay.relay_return_path(self) or ''

    @property
    def reverse_return_path(self):
        '''Return-Path for Reverse for Relay

        - used for forwarding error message for Relayed message
        '''
        return self.relay and self.relay.reverse_return_path(self) or ''

    @property
    def relay_to(self):
        return self.relay and self.relay.postbox.forward.email

    def reverse_to(self):
        return self.relay and self.relay.sender.email

    def relay_message(self):
        if self.server and self.server.handler:
            self.server.handler.relay_message(self)

    def reverse_message(self):
        if self.server and self.server.handler:
            self.server.handler.reverse_message(self)


class Message(object):
    ''' Raw Message '''

    def process_message(self):
        if self.forwarder:
            self.forwarder.forward_message(self)
            return

        if self.bounced_recipient:
            self.bounced_recipient.bounce(
                status='smtp bounce',
                message=self.raw_message)
            return

        if self.original_message:
            self.original_message.bounce_back(self)
            return

    @property
    def forwarder(self):
        def _cache():
            self._forwarder = self.forwarder_model.objects.filter(
                address=self.recipient).first()
            return self._forwarder
        return getattr(self, '_forwarder', _cache())

    @property
    def original_message(self):
        def _cache():
            self._original_message = self._meta.model.objects.filter(
                relay_from=self.recipient).first()
            return self._original_message
        return getattr(self, '_original_message', _cache())

    @property
    def bounced_recipient(self):
        def _cache():
            self._bounced_recipient = Recipient.objects.filter(
                key=self.recipient).first()
            return self._bounced_recipient
        return getattr(self, '_bounced_recipient', _cache())

    def bounce_back(self, message):
        # Bounce
        self.relay.forwarder.forward.bounce()

        # Send back error
        bounce_from = self.relay.forwarder.domain.verp()
        backends.SmtpBackend().send_raw_message(
            bounce_from,
            self.relay.sender.address, message.raw_message)
