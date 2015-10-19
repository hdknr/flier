''' Email Delivery Subsystem
'''
from django.db import models


class DomainQuerySet(models.QuerySet):
    def for_address(self, address, transport=None):
        user, domain = address.split('@')
        obj = self.filter(domain=domain).first()
        if not obj and transport:
            obj = self.create(domain=domain, transport=transport)
        return obj


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
    pass
