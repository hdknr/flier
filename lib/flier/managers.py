from django.db import models
from django.utils.timezone import now


class RecipientStatusQuerySet(models.QuerySet):
    def get_status(self, code, label=None):
        status, created = self.get_or_create(code=code)
        if created:
            status.label = label or code
            status.save()
        return status


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

    def active_set(self):
        return self.filter(
            sent_at__isnull=True, to__enabled=True)
