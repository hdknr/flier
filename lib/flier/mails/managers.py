from django.db import models
from django.utils.timezone import now

import utils


class MailTemplateQuerySet(models.QuerySet):
    def load_for_name(self, name):
        obj = self.filter(name=name).first()
        if not obj:
            source, path = utils.get_template_source(name)
            text = source or "subject\nbody"
            subject, text = text.split('\n', 1)

            obj = self.objects.create(
                name=name, subject=subject, text=text)

        return obj


class MailQuerySet(models.QuerySet):
    def queueing_set(self, basetime=None):
        basetime = basetime or now()
        return self.filter(
            models.Q(due_at__isnull=True) | models.Q(due_at__lte=basetime),
            status=self.model.STATUS_QUEUED,
            sent_at__isnull=True,
        ).exclude(task_id__regex=r'.+')


class RecipientQuerySet(models.QuerySet):
    pass
