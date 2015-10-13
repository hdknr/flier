''' Email Delivery Subsystem
'''
from django.db import models


class RelayQuerySet(models.QuerySet):

    @property
    def forwarder_model(self):
        return self.model._meta.get_field_by_name('forwader')[0].related_model

    @property
    def sender_model(self):
        return self.model._meta.get_field_by_name('sender')[0].related_model

    def create_from_message(self, message):
        '''Create a Relay for Message if forwareder exists for the recipient '''

        forwarder = self.forwarder_model.objects.filter(
            address=message.recipient).first()

        if not forwarder:
            return None

        sender, created = self.sender_model.objects.get_or_create(
            address=message.sender)

        relay, created = self.get_or_create(
            forwarder=forwarder, sender=sender)

        return relay


class MessageQuerySet(models.QuerySet):
    def find_original_message(self, message):
        params = message.bounced_parameters
        args = params['args']
        if params['handler'] in ['relay', 'reverse', ] and len(args) == 2:
            return self.filter(id=args[1], relay__id=args[0]).first()
