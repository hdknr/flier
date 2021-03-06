'''
AWS SES

- http://boto.readthedocs.org/en/latest/ref/ses.html
'''
from django.core.mail.message import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
import json
from datetime import datetime
from enum import Enum

import boto.ses
import requests
from . import aws, defs
import backends

import traceback
from logging import getLogger
logger = getLogger('flier')


class BaseObjectSerializer(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, object):
            return ''

        return super(BaseObjectSerializer, self).default(obj)

    @classmethod
    def dumps(cls, obj, *args, **kwargs):
        kwargs['cls'] = cls
        return json.dumps(obj, *args, **kwargs)


class Service(object):

    def cert(self, url):
        cert = self.certificate_set.filter(cert_url=url).first()
        if not cert:
            cert = self.certificate_set.create(
                cert_url=url,
                cert=requests.get(url).text)
        return cert

    @property
    def regions(self):
        def _cache():
            self._regions = aws.get_ses_regions()
            return self._regions

        return getattr(self, '_regions', _cache())

    @property
    def region_info(self):
        def _cache():
            self._region_info = None
            for ri in self.regions:
                if ri.name == self.region:
                    self._region_info = ri
                    break

            return self._region_info

        return getattr(self, '_region_info', _cache())

    @property
    def connection(self):
        def _cache():
            self._conn = boto.connect_ses(
                aws_access_key_id=self.key,
                aws_secret_access_key=self.secret,
                region=self.region_info)
            return self._conn

        return getattr(self, '_conn', _cache())

    @property
    def sns_connection(self):
        def _cache():
            regions = aws.get_sns_regions(self.region)
            self._conn_sns = boto.connect_sns(
                aws_access_key_id=self.key,
                aws_secret_access_key=self.secret,
                region=regions[0])
            return self._conn_sns

        return getattr(self, '_conn_sns', _cache())

    def verify_email_address(self, email):
        '''
        Verifies an email address.
        This action causes a confirmation email message
        to be sent to the specified address.
        '''
        addresses = self.list_verified_email_addresses()
        if email not in addresses:
            res = self.connection.verify_email_address(email)
            return res

    def list_verified_email_addresses(self):
        '''
        A ListVerifiedEmailAddressesResponse structure.
        Note that keys must be unicode strings.
        '''
        data = self.connection.list_verified_email_addresses()
        res = aws.ListVerifiedEmailAddressesResponse(data)
        return res.addresses


class Source(object):
    @property
    def connection(self):
        return self.service.connection

    @property
    def backend(self):
        return backends.SesBackend(connection=self.connection)

    @property
    def instance(self):
        return self

    def cert(self, url):
        return self.service.cert(url)

    def send_raw_message(self, addr_from, addr_to, raw_message):
        if self.enabled:
            self.connection.send_raw_email(
                raw_message=raw_message,
                source=addr_from,
                destinations=addr_to,
            )

    def verify_address(self, address=None):
        '''
        http://boto.readthedocs.org/en/latest/ses_tut.html
        #verifying-a-sender-email-address
        '''
        address = address or self.address
        if address:
            self.connection.verify_email_address(address)

    def set_notification(self):
        '''
        http://boto.readthedocs.org/en/latest/ref/ses.html?
        highlight=ses
        #boto.ses.connection.SESConnection.set_identity_notification_topic
        '''
        for topic in self.topic_set.all():
            self.connection.set_identity_notification_topic(
                self.address,
                topic.NOTIFICATION_TYPES[topic.topic],
                topic.arn)
            # TOOD: ERROR HANDLING

    def create_message(self, *args, **kwargs):
        if self.enabled:
            return EmailMultiAlternatives(
                from_email=self.address,            # Only Verified Address
                connection=self.backend,            # IMPORTANT: SesBackend
                *args, **kwargs
            )

    def create_topic(self, notification, site=None, scheme='http'):
        site = site or Site.objects.first()
        if notification in defs.Topic.NOTIFICATION_TYPES:
            topic = defs.Topic.NOTIFICATION_TYPES.index(notification)
            topic_name = u"{}-{}-topic".format(
                self.service.name, notification)
            endpoint = u"{}://{}{}".format(
                scheme, site.domain,
                reverse('flierses_notify',
                        kwargs={'topic': notification}))
            arn = aws.create_ses_notification(
                self.service.sns_connection,
                self.service.connection,
                topic_name, endpoint, self.address, notification)

            if not self.topic_set.filter(topic=topic).update(arn=arn):
                self.topic_set.create(topic=topic, arn=arn)


class Notification(object):

    @property
    def message_object(self):
        def _cache():
            self._message_object = aws.SnsMessage(self.message)
            return self._message_object

        return getattr(self, '_message_object', _cache())

    @property
    def headers_object(self):
        def _cache():
            self._headers_object = json.loads(self.headers)
            return self._headers_object

        return getattr(self, '_headers_object', _cache())

    @property
    def _topic(self):
        if not self.topic_id:
            field = self._meta.get_field('topic')
            self.topic = field.related_model.objects.filter(
                arn=self.message_object.TopicArn).first()
            if self.topic:
                self.save()
        return self.topic_id and self.topic

    @property
    def cert(self):
        topic = self._topic
        return topic.source.cert(self.message_object.SigningCertURL)

    def is_valid(self):
        cert = self.cert
        return self.message_object.verify(cert.cert)

    def signal(self):
        signal = None
        if self.message_object.Type in [
            'SubscriptionConfirmation', 'UnsubscribeConfirmation'
        ]:
            signal = self.confirm_signal
        elif self.message_object.Type in ['Notification']:
            signal = dict(
                Complaint=self.complaint_signal,
                Bounce=self.bounce_signal,
                Delivery=self.delivery_signal,
            ).get(self.message_object.Message.notificationType, None)

        try:
            signal and signal.send(sender=type(self), instance=self)
        except:
            logger.error(traceback.format_exc())

    def confirm(self):
        self.message_object.confirm_subscribe_url()

    def get_address_list(self):
        return self.message_object.get_address_list()

    def get_message(self):
        return self.message


class Certificate(object):
    pass
