''' Email Delivery Subsystem
'''
from django.db import models
from email.utils import parseaddr
from email import message_from_file
from logging import getLogger
import traceback
logger = getLogger('flier')


class DomainQuerySet(models.QuerySet):
    def for_address(self, address, transport=None):
        ''' return Domain object instance for a given email address
        '''
        user, domain = address.split('@')
        obj = self.filter(domain=domain).first()
        if not obj and transport:
            obj = self.create(domain=domain, transport=transport)
        return obj


class SmtpSenderQuerySet(models.QuerySet):
    def for_address(self, address, name=None):
        dom_field = self.model._meta.get_field('domain')
        dom = dom_field.related_model.objects.for_address(address)
        sender = dom.smtpsender_set.filter(address=address).first()
        if not sender:
            sender = dom.smtpsender_set.create(
                address=address, name=name or address)
        return sender


class ForwarderQuerySet(models.QuerySet):
    def update_or_create(self, domain, address, forward):
        '''
        :param str address:
        :param Address forward:
        '''
        obj = self.filter(address=address).first()
        if not obj:
            return self.create(
                domain=domain, address=address, forward=forward)
        if obj.forward != forward:
            obj.forward = forward
            obj.save()
        return obj

    def find_destination(self, address):
        '''Forwading address or Address if valid'''
        from flier.models import Address
        forwarder = self.filter(address=address).first()
        return forwarder and forwarder.forward or Address.get_on_valid(address)


class RelayQuerySet(models.QuerySet):
    pass


class MessageQuerySet(models.QuerySet):
    def from_file(self, path, **kwargs):
        return self.from_mailobject(message_from_file(open(path)), **kwargs)

    def from_mailobject(self, obj, **kwargs):
        '''
            :param email.message.Message obj:
        '''

        try:
            _, from_address = parseaddr(
                obj['Return-Path'] or obj['From'])
            _, to_address = parseaddr(
                obj['Delivered-To'] or obj['To'])

            doms = self.model._meta.get_field('domain').related_model
            domain = doms.objects.filter(
                domain=to_address.split('@')[1]).first()
            return self.create(
                domain=domain, sender=from_address, recipient=to_address,
                original_recipient=to_address, raw_message=obj.as_string(),
                **kwargs)
        except:
            logger.error(traceback.format_exc())
