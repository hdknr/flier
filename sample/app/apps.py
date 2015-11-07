# -*- coding: utf-8 -*-
from django.apps import AppConfig as DjangoAppConfig
from django.utils.translation import (
    ugettext_lazy as _,
)


# celery -A app.apps.celery worker -l info -B

from djasync.queue import CeleryModule
celery = CeleryModule(__file__)


class AppConfig(DjangoAppConfig):
    name = 'app'
    verbose_name = _("Application")

    def ready(self):
        # for shared_task
        self.celery = celery.app
