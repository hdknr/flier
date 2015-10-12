from django.db import models
from django.utils.timezone import now


class RecipientQuerySet(models.QuerySet):
    def send_status(self, sender, to, message_id, key,
                    status='Sent', message=''):

        recipient, c = self.get_or_create(
            message_id=message_id, sender=sender, to=to)

        recipient.key = key
        recipient.sent_at = now()
        recipient.status = status
        recipient.message = message
        recipient.save()

        return recipient

    def send_failed_status(self, sender, to, message_id, status, message):
        recipient, c = self.get_or_create(
            message_id=message_id, sender=sender, to=to)

        recipient.sent_at = now()
        recipient.status = status
        recipient.message = message
        recipient.save()

        return recipient
