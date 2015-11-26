''' Email Delivery Subsystem
'''
from django.db import models
from email.utils import parseaddr
from email import message_from_file


class DomainQuerySet(models.QuerySet):
    def for_address(self, address, transport=None):
        user, domain = address.split('@')
        obj = self.filter(domain=domain).first()
        if not obj and transport:
            obj = self.create(domain=domain, transport=transport)
        return obj


class SenderQuerySet(models.QuerySet):
    def for_address(self, address, name=None):
        dom_field = self.model._meta.get_field_by_name('domain')[0]
        dom = dom_field.related_model.objects.for_address(address)
        sender = dom.sender_set.filter(address=address).first()
        if not sender:
            sender = dom.sender_set.create(
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


class RelayQuerySet(models.QuerySet):
    pass


class MessageQuerySet(models.QuerySet):
    def from_file(self, path):
        return self.from_mailobject(message_from_file(open(path)))

    def from_mailobject(self, obj):
        '''
            :param email.message.Message obj:
        '''

        _, from_address = parseaddr(obj['Return-Path'])
        _, to_address = parseaddr(obj['Delivered-To'])
        doms = self.model._meta.get_field_by_name('domain')[0].related_model
        domain = doms.objects.filter(domain=to_address.split('@')[1]).first()
        return self.create(
            domain=domain, sender=from_address, recipient=to_address,
            original_recipient=to_address, raw_message=obj.as_string())
