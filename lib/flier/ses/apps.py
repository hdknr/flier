from django.apps import AppConfig as DjangoAppConfig
from django.utils.translation import (
    ugettext_lazy as _,
)


class AppConfig(DjangoAppConfig):
    name = 'ses'
    verbose_name = _("Flier SES")

    def ready(self):
        import tasks        # NOQA
